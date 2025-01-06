# 1. 
# GCP Report Analyzer

## Overview

**GCP Report Analyzer** is a Python-based utility for processing Google Cloud Platform (GCP) reports. This tool provides an enhanced analysis of GCP services, focusing on categorizing compliant and non-compliant findings, generating summaries, and creating a detailed report in Excel format. It is designed to streamline compliance audits and architectural reviews.

## Features

- Supports GCP report files in CSV and Excel formats.
- Categorizes findings into **Compliant** and **Non-Compliant**.
- Generates detailed summaries of issues by service, control titles, and projects affected.
- Produces a well-structured Excel report with:
  - Non-compliant and compliant findings.
  - Summary tables with zebra striping for improved readability.
  - Service-level analysis of issues, resources, and projects affected.
- Flexible data handling with built-in validation for required columns and error handling for unsupported formats.

## File Structure

```plaintext
project_directory/
├── main.py                  # Main script to execute the program
├── README.md                # Documentation
├── requirements.txt         # Dependencies
```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/gcp-report-analyzer.git
   cd gcp-report-analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have Python 3.7+ installed.

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. Enter the GCP report file name when prompted. Ensure the file is in the same directory as the script or provide the full path.

3. The script will process the file and generate an enhanced Excel report in the same directory.

### Input File Requirements

- File format: **CSV** or **Excel** (`.xlsx`).
- Required columns:
  - `service`
  - `title`
  - `status`
  - `control_title`
  - `control_description`
  - `reason`
  - `resource`
  - `project`
  - `location`

### Output

The tool generates an enhanced Excel report with the following sheets:

1. **Report_pp**:
   - Raw data extracted from the input file.

2. **Consolidated**:
   - Non-compliant findings section (highlighted in red).
   - Compliant findings section (highlighted in green).

3. **Service Analysis**:
   - Aggregated analysis of issues by service, projects affected, and total resources.

4. **Summary Tables**:
   - Non-compliant and compliant summary tables with zebra striping.

## Error Handling

- If the input file format is not CSV or Excel, an error message is displayed.
- Missing required columns will raise an error with a detailed message.
- NaN or infinite values in the input data are gracefully handled.

## Example

### Input
An example GCP report in CSV format:
```csv
service,title,status,control_title,control_description,reason,resource,project,location
Compute,Instance Alert,alarm,Instance Monitoring,Check instance logs,Missing logs,instance-1,project-a,us-central1
Storage,Bucket Alert,ok,Bucket Security,Ensure bucket permissions,NA,bucket-1,project-b,us-east1
```

### Output
The generated Excel report includes:
- Detailed issue categorization.
- Service-level issue analysis.
- Summary tables for compliant and non-compliant findings.

## Dependencies

- Python 3.7+
- pandas
- openpyxl
- numpy
- xlsxwriter

Install dependencies using:
```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
