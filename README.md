# BlinkIT Grocery Sales Analysis

## What this project does
This Python data analytics project uses the supplied `BlinkIT Grocery Data.xlsx` workbook and follows the Sapphire IQ project brief. It checks data quality, summarizes sales by item type/outlet/location, and creates charts.

## Requirements
- Python 3.10 or later
- pandas
- openpyxl
- matplotlib

## How to run
1. Install Python if it is not already installed.
2. Keep `run_analysis.py` and `BlinkIT Grocery Data.xlsx` in the same folder.
3. Open Command Prompt/Terminal in that folder.
4. Install dependencies:
   `python -m pip install pandas openpyxl matplotlib`
5. Run:
   `python run_analysis.py`
6. Check the `outputs` folder for cleaned data, summary CSV files, and charts.

## Files
- `run_analysis.py` — complete analysis script.
- `BlinkIT Grocery Data.xlsx` — original source dataset.
- `outputs/blinkit_cleaned_data.csv` — cleaned data after exact duplicate removal and label standardization.
- `outputs/sales_by_*.csv` — group summaries.
- `outputs/charts/` — generated visualizations.
- `outputs/project_report.md` — report based on the current workbook.

## Important note
This is a sales data analysis project, not an online grocery ordering app. Results are descriptive, not proof of cause and effect. Missing values are not filled with made-up data.
