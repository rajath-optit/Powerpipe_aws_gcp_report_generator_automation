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

# 2 Two_analyse.py
### Project Name: **AWS Compliance Reporting Tool**

---

### Overview:
The **AWS Compliance Reporting Tool** helps you generate comprehensive AWS compliance reports from raw CSV/Excel files. This tool processes compliance data, enriches it with priority annotations, generates detailed Excel reports, and visualizes key insights such as priority distribution, service risk, and more. The generated report can then be used in a subsequent program for document generation (Word document).

### Features:
- **Data Enrichment**: Enriches raw compliance data with priority annotations and recommendations based on control titles.
- **Multiple Sheet Analysis**: Generates multiple Excel sheets for detailed insights:
    - Raw Data
    - Open Issues
    - No Open Issues
    - Service Category Analysis
    - Priority Summary
    - Pivot Tables and Analysis
    - Visualization Techniques
    - Advanced Configuration Details
- **Excel Formatting**: Automatically formats sheets with color coding based on priority (High, Medium, Low, Safe).
- **Service Category Breakdown**: Categorizes and aggregates data by AWS service (e.g., Security, Compute, Storage, etc.).
- **Visualization Insights**: Provides suggestions for visualizing the compliance data using heatmaps, radar charts, and treemaps.

---

### Prerequisites:
1. Python 3.x
2. Required Python libraries:
   - `pandas`
   - `openpyxl`
   - `xlsxwriter`
3. Input files:
   - Compliance report file in CSV/Excel format.
   - Priority annotations Excel file (e.g., `PowerPipeControls_Annotations.xlsx`).

---

### Usage:

#### Step 1: Generate a Comprehensive Excel Report

The **AWS Compliance Reporting Tool** processes raw compliance data, enriches it with priority annotations, and generates an Excel report. Run the program as follows:

```bash
python3 2_ana.py
```

**Input Prompts:**
- **Enter input compliance report file (CSV/Excel):** Enter the path to the raw CSV or Excel file.
- **Enter priority annotations file (default: PowerPipeControls_Annotations.xlsx):** Enter the path to the priority annotations file (default is `PowerPipeControls_Annotations.xlsx`).

**Output:**  
A comprehensive Excel report will be generated with the following sheets:
- Raw Data
- No Open Issues
- Open Issues
- Service Category Analysis
- Priority Summary
- Service Pivot
- Visualization Techniques
- Advanced Configuration

---

#### Step 2: Generate the Word Report

Once the comprehensive Excel report is generated, use the second program to convert it into a Word document. Run the following command:

```bash
python3 3_doc.py
```

**Input Prompts:**
- **Enter the path to the Excel compliance report:** Enter the path to the Excel file generated in Step 1.
- **Enter the client name:** Enter the name of the client for the report.
- **Enter the link to the detailed services Excel:** Enter the link to the detailed services Excel file (for references in the report).

**Output:**  
A Word document will be generated with the name format:
```
<base_name>_comprehensive_report_<timestamp>_report.docx
```

---

### Example Flow:

1. Run the **AWS Compliance Reporting Tool**:
   ```bash
   python3 2_ana.py
   ```
   Enter the input file (e.g., `1_pp_raw_powerpipe.csv`) and priority file (e.g., `PowerPipeControls_Annotations.xlsx`). This generates an Excel file:
   ```
   1_pp_raw_powerpipe_comprehensive_report_20250107_054500.xlsx
   ```

2. Run the second program to generate the Word document:
   ```bash
   python3 3_doc.py
   ```
   Enter the path to the generated Excel report and other required information. This generates a Word document:
   ```
   1_pp_raw_powerpipe_comprehensive_report_20250107_054500_report.docx
   ```

---

### File Structure:

- **2_ana.py** - Main Python script for generating comprehensive Excel reports.
- **3_doc.py** - Python script for converting the Excel report into a Word document.
- **PowerPipeControls_Annotations.xlsx** - Priority annotation file (you can use your own or modify this template).
- **example_input.csv** - Example input file (CSV format).
- **example_input.xlsx** - Example input file (Excel format).

---

### Template for Word Document Generation:

- The second program (**3_doc.py**) takes the Excel report and additional inputs to generate a Word report based on the provided template.  
You can customize the template to format the final report as needed.

---

### License:
This tool is provided "as-is" for educational and internal use only. It is not responsible for any data loss or errors generated during processing.

---

### Future Enhancements:
- Add support for other data sources (e.g., JSON, SQL).
- Allow for more custom formatting options in the Excel reports.
- Integrate more visualization techniques (e.g., pie charts, line graphs).

--- 

With these steps, you now have a powerful tool for processing AWS compliance reports and generating comprehensive reports with detailed analysis.

# 3.Three_Document_creator.py
Here is the README for the Python script `Three_Document_creator.py`:

---

# **Three_Document_creator.py**

### **Overview**
`Three_Document_creator.py` is a Python script designed to generate a comprehensive AWS Compliance Report in the form of a Word document (`.docx`) from an Excel-based compliance report. The script extracts data, generates charts, and presents a detailed summary with various sections, including tables, graphs, and detailed AWS service descriptions.

The script is intended for AWS security and compliance assessments, providing an overview of resources, priority levels, and compliance status. It formats this information into a polished report that can be shared with clients.

### **Features**
- **Excel Data Extraction**: The script reads data from an Excel file to generate tables and charts.
- **Dynamic Charts**: Matplotlib is used to generate visual charts based on the data from specific sheets.
- **Table Formatting**: Tables are formatted with color-coded priority levels for better readability.
- **Title and Index Pages**: Automatically generated title page and index for a professional layout.
- **Service Breakdown**: Provides detailed descriptions and analysis for various AWS services.
- **Hyperlinks**: Links to detailed reports or other resources are embedded in the document.
- **Report Sections**: The report includes various sections like overview, graphs, service analysis, compliance summary, and more.

### **Requirements**
To run this script, you will need to install the following Python packages:

- `openpyxl`: For reading and writing Excel files.
- `docx`: For creating and editing Word documents.
- `matplotlib`: For generating charts.
- `pandas`: For data manipulation.
- `datetime`: For adding timestamps to the report.

You can install these dependencies using pip:

```bash
pip install openpyxl python-docx matplotlib pandas
```

### **Usage**
1. **Prepare Excel Data**: Ensure your Excel file has relevant data related to AWS compliance. The script works with sheets named "Priority Summary", "Service Pivot", and other analysis sheets.
2. **Run the Script**: Execute the script from your command line. You will be prompted to enter the following:
   - **Excel file path**: The path to the Excel file containing the compliance data.
   - **Client name**: The name of the client for whom the report is being generated.
   - **Services link**: A link to the detailed services report (usually another Excel file).
   
   Example:
   ```bash
   Enter the path to the Excel compliance report: /path/to/excel_report.xlsx
   Enter the client name: XYZ Corporation
   Enter the link to the detailed services Excel: https://www.example.com/detailed_report
   ```

3. **Report Generation**: After entering the required information, the script will generate a Word document (`.docx`) with the following sections:
   - **Title Page**: Report title and metadata.
   - **Index Page**: An index table with page numbers.
   - **Overview**: General explanation of AWS compliance evaluation.
   - **Service Analysis**: Detailed analysis of AWS services, along with any visual charts and tables.
   - **Detailed Report Link**: A link to the detailed compliance report and other resources.
   - **Synopsis and Conclusion**: A synopsis of the findings and a conclusion with security recommendations.

4. **Output**: The generated report will be saved in the same directory as the input Excel file, with the name `report.docx`.

### **Functionality Breakdown**
- **ComplianceReportDocumentGenerator Class**: This class handles the logic for creating the report.
  - **`__init__()`**: Initializes the class with the Excel file path, client name, and services link.
  - **`_create_chart_from_excel_data()`**: Generates charts from data in the Excel file.
  - **`_create_title_page()`**: Creates the title page with the report details and index.
  - **`_add_table_to_doc()`**: Adds formatted tables to the Word document.
  - **`generate_comprehensive_report()`**: Orchestrates the report generation, including adding sections like overview, charts, tables, and analysis.
  - **`_extract_table_data()`**: Extracts data from a specified sheet in the Excel file.

### **Sample Output**

The output Word document (`.docx`) will contain:

- A **Title Page**: Contains the client name, report name, date, and version.
- **Index**: Lists the sections in the report and corresponding page numbers.
- **Overview**: Provides a brief explanation of AWS compliance and the purpose of the report.
- **Service Analysis**: A section where data is analyzed, including charts and tables representing the compliance status of various AWS services.
- **Graph Analysis**: Visual representation of AWS compliance data in a graph.
- **Link to Detailed Report**: A link to further detailed data, usually hosted elsewhere.
- **Synopsis and Conclusion**: High-level summaries and recommendations based on the report findings.

### **Customization**
The script can be modified to support additional or custom Excel sheets. You can adjust the way the charts are generated and modify the report sections to suit your needs.

### **Example Output File**:
```bash
XYZ_Corporation_report.docx
```

This file will be saved in the same directory as your input Excel file.

### **Conclusion**
`Three_Document_creator.py` is a powerful automation tool for generating professional AWS compliance reports directly from Excel data. It simplifies the reporting process and ensures that all the necessary details are neatly organized in a user-friendly document.

### **License**
This script is open-source and can be modified or distributed under the MIT license.

---
