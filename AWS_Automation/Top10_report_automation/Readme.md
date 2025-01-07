# README for PowerPipe Top 10 Report Generator

## Overview
The **PowerPipe Top 10 Report Generator** script processes control data from a given input file (CSV or Excel format) and annotates the information with priority levels and recommended actions, leveraging a database (Excel format). The script outputs a new Excel file that organizes the data into multiple sheets based on compliance status, applies color-coded priority labels, and generates charts and pivot tables to visualize compliance vs non-compliance.

## Features
- **Input file format support**: CSV or Excel files
- **Prioritization**: Control titles are matched with priorities (High, Medium, Low) and corresponding recommendations.
- **Color-coding**: Excel cells are color-coded based on priority:
  - Green: Safe/Well Architected (status: ok, info, or skip)
  - Red: High Priority
  - Orange: Medium Priority
  - Yellow: Low Priority
- **Output File**: A timestamped Excel file that includes:
  - Compliance vs. Non-Compliance sheets
  - Pivot tables to visualize counts of issues by status and control title
  - Line charts representing the counts of compliance and non-compliance issues
- **Fixed Flag**: A checkbox for each control indicating whether the issue has been fixed, depending on the control's status.

## Requirements
- Python 3.x
- **Libraries**:
  - `pandas` for data manipulation
  - `openpyxl` for working with Excel files
  - `datetime` for generating timestamped output filenames

You can install the necessary Python libraries using pip:

```bash
pip install pandas openpyxl
```

## Usage
1. **Prepare your input files**:
   - **Input File**: A CSV or Excel file containing control data with columns like `control_title`, `control_description`, `status`, etc.
   - **Priority File**: A pre-existing Excel file (`PowerPipeControls_Annotations.xlsx`) that contains control titles along with their assigned priorities and recommended steps. 

2. **Run the script**:
   - Execute the script by running it in your Python environment.
   - The script will prompt you to enter the input file name (CSV or Excel).
   
3. **Output**:
   - The script generates a new Excel file with the following sheets:
     - `All Data`: The full list of controls, updated with priorities and recommendations.
     - `Compliance`: A sheet with controls marked as compliant (status: ok, info, or skip).
     - `Non-Compliance`: A sheet with controls marked as non-compliant (status: alarm).
     - `Compliance Pivot`: A pivot table summarizing the compliance issues.
     - `Non-Compliance Pivot`: A pivot table summarizing the non-compliance issues.
   - The output file is timestamped and saved in the same directory as the input file.

## Example of Script Execution

```bash
$ python powerpipe_report_generator.py
Enter the input file name (CSV or Excel): control_data.xlsx
Updated file saved as control_data_updated_20250107_123456.xlsx
```

This would generate a file `control_data_updated_20250107_123456.xlsx` with all the relevant updates, including charts, formatted priority labels, and pivot tables.

## Notes
- The script works based on matching the `control_title` from the input file with the priority data from the provided priority file. If no match is found, a default value is used.
- It is essential that the `PowerPipeControls_Annotations.xlsx` file is available and contains correct data in the required columns (e.g., `control_title`, `priority`, `Recommendation Steps/Approach`).
- If a control's status is "alarm", it is marked as non-compliant, and the checkbox for "Fixed" is set to False.
  
## Troubleshooting
- **File format issues**: Ensure the input file is either CSV or Excel format. The script does not support other formats.
- **Missing priority data**: If the `control_title` does not exist in the priority file, it will receive a "No data" priority and recommendation.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
