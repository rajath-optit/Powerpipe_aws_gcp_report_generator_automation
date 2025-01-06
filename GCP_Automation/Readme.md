# 1
Enhanced GCP Report Processing Script

Overview

This Python script processes and enhances GCP (Google Cloud Platform) compliance reports. It provides a comprehensive analysis of compliant and non-compliant findings, creates summaries, and outputs an organized Excel report.

Features

Support for CSV and Excel Input Files: Automatically detects and processes .csv or .xlsx files.

Data Categorization: Separates data into compliant and non-compliant categories for easier analysis.

Detailed Service Analysis: Groups and summarizes issues by GCP services.

Enhanced Reporting: Generates an Excel file with formatted sheets for raw data, consolidated findings, and detailed summaries.

Custom Formatting:

Zebra striping for better readability.

Priority-based formatting.

Section headers with color coding.

Automated Summary Tables: Summarizes compliant and non-compliant findings for quick review.

Requirements

Python Dependencies

Ensure the following Python packages are installed:

pandas

numpy

openpyxl

xlsxwriter

Install these dependencies using pip:

pip install pandas numpy openpyxl xlsxwriter

Input File

The input file must be in CSV or Excel format and contain the following required columns:

service

title

status

control_title

control_description

reason

resource

project

location

Output File

The script generates an enhanced report as an Excel file with the following sheets:

Report_pp: Raw input data.

Consolidated: Compliant and non-compliant findings.

Service Analysis: Issues grouped by GCP service.

Summary Tables: Summarized findings with zebra striping and priority formatting.

Usage

Running the Script

Save the script as a .py file, e.g., gcp_report_processor.py.

Execute the script in a terminal or command prompt:

python gcp_report_processor.py

Enter the file name of the GCP report when prompted.

The script processes the file and saves the enhanced report in the same directory as the script.

Example

Input:

File name: gcp_report.csv

Example content:

service,title,status,control_title,control_description,reason,resource,project,location
Compute,High CPU Usage,alarm,CPU Monitoring,Monitor CPU usage regularly,Threshold exceeded,vm-instance-1,project-id-123,us-central1
Storage,Secure Access,ok,Data Security,Ensure data encryption at rest,Compliant,bucket-1,project-id-456,us-east1

Output:

Enhanced report: gcp_report_enhanced_report_<timestamp>.xlsx

Output Breakdown

Raw Data (Report_pp): Contains all the original data from the input file.

Consolidated Findings:

Non-compliant findings with actionable columns: Feedback, Action Items, Priority, etc.

Compliant findings with a summary of well-architected resources.

Service Analysis: Aggregated issues, affected projects, and resources for each service.

Summary Tables:

Non-compliant findings summary.

Compliant findings summary with Safe/Well Architected status.

Error Handling

File Format Validation: Supports only .csv or .xlsx files.

Missing Columns: The script checks for required columns and raises an error if any are missing.

File Not Found: Verifies the existence of the input file and raises an error if it is not found.

Customization

Categories: The script categorizes services into predefined groups. You can modify the categories dictionary to fit specific needs.

Column Formatting: Adjust the formats dictionary for custom Excel formatting.

License

This script is provided "as-is" without warranty of any kind. Feel free to modify and use it for personal or professional purposes.
