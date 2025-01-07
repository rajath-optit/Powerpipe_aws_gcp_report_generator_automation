# PowerPipe AWS Security Report Processor

This Python script is designed to process the AWS security report (e.g., `aws_top_10.benchmark.account_security`), match each control title with a priority and recommendation from a predefined database, and produce a detailed report with color-coded priorities, feedback options, and fixed checkboxes. The output is saved as a timestamped Excel file with compliance and non-compliance information separated into different sheets.

---

## Requirements

- **Python 3.x** (Recommended: Python 3.6 or higher)
- **Libraries:**
  - pandas
  - openpyxl
  - datetime

You can install the required libraries using the following command:

```bash
pip install pandas openpyxl
```

---

## File Structure

Ensure the following files are available in the same directory as the script:

1. **PowerPipe_Control_Annotations.xlsx**  
   This is the database file that contains control titles, priority, and recommendations for different security controls. The script will match the control titles in the AWS security report with those listed in this file.

2. **AWS Report (CSV/Excel)**  
   The AWS security report file (e.g., `aws_top_10.benchmark.account_security.csv` or `.xlsx`). This is the file you download from PowerPipe. The script will process this file to extract control titles, statuses, and then populate additional information such as priority and recommendations.

---

## Script Functionality

### 1. Loading Data

The script allows you to input an AWS report file (either `.csv` or `.xlsx`) and a priority database (`PowerPipe_Control_Annotations.xlsx`). The report is processed and matched with the priorities in the database.

```python
df_input, df_priority = load_data(input_file, priority_file)
```

### 2. Processing Control Titles

- The script iterates over the controls in the AWS report and tries to match each `control_title` to the corresponding entry in the priority database.
- Based on the status (`ok`, `info`, `skip`, `alarm`), it assigns the correct priority (`High`, `Medium`, `Low`, or `Safe/Well Architected`), and includes a corresponding recommendation in the report.

```python
updated_df = update_priority_and_recommendation(df_input, df_priority)
```

### 3. Color Coding Priorities

- **Green**: Safe/Well Architected (status: `ok`, `info`, `skip`)
- **Red**: High Priority (for non-compliant controls)
- **Orange**: Medium Priority
- **Yellow**: Low Priority

The priorities are color-coded in the Excel output for easy identification.

### 4. Output Format

The script generates a new Excel file with the following sheets:

- **All Data**: All control data, including status, priority, and recommendations, with the priority column color-coded.
- **Compliance**: Controls with statuses `ok`, `info`, or `skip`.
- **Non-Compliance**: Controls with the status `alarm`.
- **Compliance Pivot**: Pivot table showing compliance counts for each control title.
- **Non-Compliance Pivot**: Pivot table showing non-compliance counts for each control title.

Additionally, the script generates line charts in both the **Compliance** and **Non-Compliance** sheets to visualize compliance issues over control titles.

### 5. Feedback and Fixed Checkboxes

- A **Feedback** column is added to each row where the user can provide feedback for each control.
- A **Fixed** checkbox is set to `False` if the status is `alarm`, otherwise, it is set to `True`.

---

## How to Use

### Step 1: Download the AWS Security Report

1. Download the AWS security report, such as `aws_top_10.benchmark.account_security.csv` or `aws_top_10.benchmark.account_security.xlsx`, from PowerPipe.
2. Place this report in the same directory as the script.

### Step 2: Place the Control Annotations File

Ensure that the `PowerPipe_Control_Annotations.xlsx` file (which contains the priority and recommendations for each control) is also in the same directory.

### Step 3: Run the Script

1. Open a terminal or command prompt in the directory containing the script and the required files.
2. Run the Python script:

```bash
python PowerPipe_AWS_Security_Report_Processor.py
```

3. Enter the input file name when prompted (e.g., `aws_top_10.benchmark.account_security.xlsx` or `.csv`).

### Step 4: Check the Output

Once the script completes, you will receive a timestamped Excel file (e.g., `aws_top_10.benchmark.account_security_updated_20250107_152435.xlsx`) containing:

- **All Data**: A full report with color-coded priorities and recommendations.
- **Compliance**: Controls with `ok`, `info`, or `skip` status.
- **Non-Compliance**: Controls with `alarm` status.
- **Pivot Tables**: A pivot table for compliance and non-compliance counts.
- **Charts**: Line charts displaying the compliance status for each control title.

---

## Example Output

- **Compliance Data**:

| Control Title | Control Description | Priority | Recommendation | Status | Feedback | Fixed |
|---------------|---------------------|----------|----------------|--------|----------|-------|
| Control 1     | Description 1        | High     | Recommendation 1 | ok     |          | True  |
| Control 2     | Description 2        | Medium   | Recommendation 2 | info   |          | True  |

- **Pivot Table (Compliance)**:

| Control Title | ok | info | skip |
|---------------|----|------|------|
| Control 1     | 1  | 0    | 0    |
| Control 2     | 0  | 1    | 0    |

- **Charts**: Line charts visualizing the counts for compliance and non-compliance.

---

## Customization

You can customize the following parameters in the script:

- **Color Fill Definitions**: Modify the color fills for each priority level by changing the `green_fill`, `red_fill`, `orange_fill`, and `yellow_fill` variables.
- **Priority and Recommendation Matching**: The script matches control titles to priorities and recommendations in the `PowerPipe_Control_Annotations.xlsx` file. Ensure that your database file is up-to-date and accurate.

---

## Troubleshooting

1. **Error: Unsupported file type**
   - Ensure the input file is either `.csv` or `.xlsx`.
   
2. **Error: No matching control title found**
   - Make sure the `control_title` in the input file matches exactly with the control titles in the `PowerPipe_Control_Annotations.xlsx` database.

3. **Empty Output**
   - Verify that the input file contains valid data and that the database file (`PowerPipe_Control_Annotations.xlsx`) is correctly structured.

---

## Conclusion

This script provides an automated and streamlined process to match AWS security control titles with a predefined priority and recommendation database, while generating a comprehensive report that is easy to analyze and visualize. The output includes detailed sheets with color-coded priorities, feedback options, and charts to help track compliance issues efficiently.

