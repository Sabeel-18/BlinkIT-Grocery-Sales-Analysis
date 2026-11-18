"""
BlinkIT Grocery Sales Analysis
Run: python run_analysis.py
Put "BlinkIT Grocery Data.xlsx" in the same folder as this script.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "BlinkIT Grocery Data.xlsx"
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Could not find {DATA_FILE.name}. Place the Excel file next to run_analysis.py."
    )

df = pd.read_excel(DATA_FILE)
df.columns = [str(c).strip() for c in df.columns]
missing = df.isna().sum()
duplicates = int(df.duplicated().sum())

for col in ["Item Fat Content", "Item Type", "Outlet Identifier", "Outlet Location Type", "Outlet Size", "Outlet Type"]:
    if col in df.columns:
        df[col] = df[col].astype("string").str.strip()
if "Item Fat Content" in df.columns:
    df["Item Fat Content"] = df["Item Fat Content"].replace({
        "LF": "Low Fat", "low fat": "Low Fat", "reg": "Regular", "regular": "Regular"
    })
for col in ["Outlet Establishment Year", "Item Visibility", "Item Weight", "Sales", "Rating"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

clean = df.drop_duplicates().copy()
clean.to_csv(OUT / "blinkit_cleaned_data.csv", index=False)

def save_group_chart(group_col, filename, title):
    summary = clean.groupby(group_col, dropna=False)["Sales"].sum().sort_values()
    plt.figure(figsize=(10, 6))
    summary.plot(kind="barh")
    plt.title(title)
    plt.xlabel("Total Sales")
    plt.ylabel(group_col)
    plt.tight_layout()
    plt.savefig(CHARTS / filename, dpi=160)
    plt.close()
    return summary

item_summary = clean.groupby("Item Type", dropna=False)["Sales"].agg(["sum", "mean", "count"]).sort_values("sum", ascending=False)
outlet_summary = clean.groupby("Outlet Type", dropna=False)["Sales"].agg(["sum", "mean", "count"]).sort_values("sum", ascending=False)
location_summary = clean.groupby("Outlet Location Type", dropna=False)["Sales"].agg(["sum", "mean", "count"]).sort_values("sum", ascending=False)
size_summary = clean.groupby("Outlet Size", dropna=False)["Sales"].agg(["sum", "mean", "count"]).sort_values("sum", ascending=False)
fat_summary = clean.groupby("Item Fat Content", dropna=False)["Sales"].agg(["sum", "mean", "count"]).sort_values("sum", ascending=False)

item_summary.to_csv(OUT / "sales_by_item_type.csv")
outlet_summary.to_csv(OUT / "sales_by_outlet_type.csv")
location_summary.to_csv(OUT / "sales_by_location.csv")
size_summary.to_csv(OUT / "sales_by_outlet_size.csv")
fat_summary.to_csv(OUT / "sales_by_fat_content.csv")

save_group_chart("Item Type", "sales_by_item_type.png", "Total Sales by Item Type")
save_group_chart("Outlet Type", "sales_by_outlet_type.png", "Total Sales by Outlet Type")
save_group_chart("Outlet Location Type", "sales_by_location.png", "Total Sales by Outlet Location")
save_group_chart("Outlet Size", "sales_by_outlet_size.png", "Total Sales by Outlet Size")

plt.figure(figsize=(8, 5))
clean.groupby("Outlet Establishment Year")["Sales"].sum().sort_index().plot(marker="o")
plt.title("Total Sales by Outlet Establishment Year")
plt.xlabel("Outlet Establishment Year")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(CHARTS / "sales_by_establishment_year.png", dpi=160)
plt.close()

plt.figure(figsize=(8, 5))
plt.scatter(clean["Item Visibility"], clean["Sales"], alpha=0.25)
plt.title("Item Visibility vs Sales")
plt.xlabel("Item Visibility")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig(CHARTS / "visibility_vs_sales.png", dpi=160)
plt.close()

print("\\nBLINKIT GROCERY SALES ANALYSIS COMPLETE")
print(f"Source rows: {len(df):,}")
print(f"Rows after exact duplicate removal: {len(clean):,}")
print(f"Exact duplicate rows found: {duplicates}")
print(f"Total sales: {clean['Sales'].sum():,.2f}")
print(f"Average sales per record: {clean['Sales'].mean():,.2f}")
print(f"Average available rating: {clean['Rating'].mean():.2f}/5")
print("\\nMissing values in source:")
print(missing.to_string())
print("\\nTop 5 item types by total sales:")
print(item_summary.head(5).round(2).to_string())
print("\\nSales by outlet type:")
print(outlet_summary.round(2).to_string())
print(f"\\nOutputs saved to: {OUT}")
