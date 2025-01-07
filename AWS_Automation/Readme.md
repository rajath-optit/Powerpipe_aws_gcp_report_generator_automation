# 1.One_ReportFormatter.py
# Enhanced PowerPipe Report Generator

## Overview

This script is designed to process and generate an enhanced PowerPipe report based on a given input file (in CSV or Excel format). The report includes categorized findings, priority levels, and recommendations, along with an organized Excel output. The script:

- Loads data from an input file (CSV/Excel).
- Loads priority data and recommendations from a predefined Excel file.
- Processes the input file by adding priority information and recommendations.
- Generates an enhanced report with categorized data, a summary of findings, and priority color formatting.
- Outputs the results to a new Excel file with a detailed report.

## Requirements

- **Python** 3.x
- **Pandas** library
- **NumPy** library
- **XlsxWriter** library
- Input file in either **CSV** or **Excel (.xlsx)** format
- Priority file in **Excel (.xlsx)** format

### Required Libraries

Ensure you have the following libraries installed:

```bash
pip install pandas numpy xlsxwriter
```

## How It Works

The script uses an input file containing a list of controls or checks and updates the file with priority information and recommendations. It then generates an Excel report with:

1. **Raw Data Sheet**: Contains the original data, updated with priority and recommendation information.
2. **Category Sheets**: Contains filtered data for each service category (e.g., Compute, Storage, Database).
3. **Summary Tables**: Contains:
   - A summary of non-compliant findings.
   - A category-wise breakdown of open issues and safe counts.

### Key Functions in the Script

#### 1. `load_data(input_file, priority_file)`
- **Purpose**: Loads the input data and priority file.
- **Inputs**:
  - `input_file`: Path to the input CSV or Excel file.
  - `priority_file`: Path to the Excel file containing priority and recommendation information.
- **Outputs**: Returns two DataFrames:
  - `df_input`: The input data (CSV/Excel).
  - `df_priority`: The priority file data.

#### 2. `update_priority_and_recommendation(df_input, df_priority)`
- **Purpose**: Updates the input data with priority and recommendation steps/approaches.
- **Inputs**:
  - `df_input`: The loaded input data.
  - `df_priority`: The priority and recommendation data.
- **Outputs**: Updated `df_input` with priority and recommendation columns filled.

#### 3. `create_enhanced_report(df_input, final_report_file)`
- **Purpose**: Creates the enhanced Excel report.
- **Inputs**:
  - `df_input`: The updated input data.
  - `final_report_file`: Path where the final report will be saved.
- **Outputs**: Writes the report to an Excel file.

#### 4. `create_category_sheets(writer, df, formats)`
- **Purpose**: Creates category-specific sheets in the final Excel report.
- **Inputs**:
  - `writer`: Excel writer object.
  - `df`: The updated input data.
  - `formats`: The formatting options for the report.
- **Outputs**: Writes category sheets to the report.

#### 5. `create_summary_tables(writer, df, formats)`
- **Purpose**: Creates the summary tables for non-compliant findings and category analysis.
- **Inputs**:
  - `writer`: Excel writer object.
  - `df`: The updated input data.
  - `formats`: The formatting options for the report.
- **Outputs**: Writes the summary tables to the report.

## Usage

1. **Prepare the Input Files**:
   - **Input File**: A CSV or Excel file containing control titles, descriptions, status, etc.
   - **Priority File**: An Excel file (`PowerPipeControls_Annotations.xlsx`) containing the priority levels (High, Medium, Low, Safe/Well Architected) and corresponding recommendation steps.

2. **Run the Script**:
   Execute the script in your Python environment:

   ```bash
   python generate_report.py
   ```

3. **Enter the Input File Name**:
   When prompted, provide the file name of the input file (CSV or Excel):

   ```
   Enter the input file name (CSV or Excel): my_input_file.xlsx
   ```

4. **Output File**:
   The script will generate an output Excel file with a timestamp in its name:

   ```
   Enhanced report generated: my_input_file_PowerPipe_Report_2025-01-07_12-30-45.xlsx
   ```

   The report will contain:
   - A raw data sheet (`Report_Raw.pp`).
   - Category sheets for each service group (e.g., Compute, Database).
   - Summary tables (`Non-Compliant Findings`, `Category Analysis`).

## File Structure

- **Input File**: The source data containing information about controls and their status.
- **Priority File**: A reference file that provides priority levels and recommendations.
- **Output File**: The generated Excel report.

## Example Input File

Your input file (CSV or Excel) should have the following columns (example):

| title    | control_title      | status  | control_description | region | account_id | resource | reason | priority | Recommendation Steps/Approach |
|----------|--------------------|---------|---------------------|--------|------------|----------|--------|----------|--------------------------------|
| Compute  | EC2 Security Check | alarm   | Check EC2 security  | us-west| 12345      | EC2      | High   | High     | Implement security measures    |
| Network  | Route 53 Config    | ok      | Check Route 53      | us-east| 67890      | Route 53 | Safe  | Safe/Well Architected | No action required             |

## Example Priority File

The priority file (`PowerPipeControls_Annotations.xlsx`) should have the following structure:

| control_title      | priority | Recommendation Steps/Approach |
|--------------------|----------|--------------------------------|
| EC2 Security Check | High     | Implement security measures    |
| Route 53 Config    | Safe     | No action required             |

## Customization

- **Categories**: You can customize the `categories` dictionary to modify the service categories.
- **Formatting**: You can modify the `formats` dictionary to customize colors, fonts, and other styling options for the report.

## License

This script is provided as-is. Feel free to modify it to suit your needs. The script does not come with any warranties.

---
