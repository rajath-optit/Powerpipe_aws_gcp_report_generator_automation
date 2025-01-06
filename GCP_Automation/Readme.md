# 1. 
# README for Enhanced GCP Report Processor

## Overview
The `create_simplified_gcp_report` script processes Google Cloud Platform (GCP) audit reports to generate detailed, well-structured Excel reports. It includes features for categorization, data analysis, compliance checking, and visualization.

## Features
- **Supports CSV and Excel Files:** Automatically detects and processes input files in `.csv` or `.xlsx` format.
- **Categorized Analysis:** Separates compliant and non-compliant findings for easier review.
- **Enhanced Summaries:** Generates service-level summaries and detailed analysis tables.
- **Custom Formatting:** Applies color-coded formatting for priority and status.
- **Zebra Striping:** Alternates row colors in summary tables for better readability.
- **Excel Output:** Saves the processed data in a user-friendly `.xlsx` format with multiple sheets.

## Requirements
- **Python Packages:**
  - `pandas`
  - `numpy`
  - `openpyxl`
  - `xlsxwriter`
- **Python Version:** Ensure Python 3.6 or higher.

## Installation
Install the required packages via pip:
```bash
pip install pandas numpy openpyxl xlsxwriter
```

## How to Use
1. **Run the Script:**
   Execute the script from the command line:
   ```bash
   python <script_name>.py
   ```
   Replace `<script_name>` with the name of the script file.

2. **Provide the Input File:**
   - When prompted, input the path to the GCP report file (CSV or Excel format).

3. **Generated Report:**
   - The script saves the enhanced report in the same directory with a timestamped filename, e.g., `report_enhanced_20250107_123456.xlsx`.

## Output Structure
The output Excel file contains the following sheets:
1. **Report_pp:** Raw input data for reference.
2. **Consolidated:** Detailed compliant and
