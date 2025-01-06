import pandas as pd
from datetime import datetime
import os
import numpy as np

# Define GCP service categories
categories = {
    'Security and Identity': ['IAM', 'KMS', 'Organization', 'Resource Manager'],
    'Compute': ['Compute', 'App Engine', 'Cloud Functions', 'Cloud Run', 'Kubernetes'],
    'Storage': ['Storage'],
    'Network': ['DNS'],
    'Database': ['AlloyDB', 'BigQuery', 'Dataproc', 'SQL'],
    'Other': ['Logging', 'Project']
}

def create_simplified_gcp_report(report_file, final_report_file):
    """
    Enhanced function to process GCP report with better analysis capabilities and error handling.
    """
    # Read input file
    try:
        if report_file.endswith('.csv'):
            raw_df = pd.read_csv(report_file)
        elif report_file.endswith('.xlsx'):
            raw_df = pd.read_excel(report_file, engine='openpyxl')
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Create working copy with required columns
    columns_to_keep = [
        'service', 'title', 'status', 'control_title', 
        'control_description', 'reason', 'resource', 
        'project', 'location'
    ]
    
    missing_columns = [col for col in columns_to_keep if col not in raw_df.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns in the input file: {missing_columns}")
    
    df = raw_df[columns_to_keep].copy()

    # Data categorization
    compliant_df = df[df['status'].isin(['ok', 'skip', 'info'])].copy()
    non_compliant_df = df[df['status'] == 'alarm'].copy()

    # Add analysis columns
    for data in [compliant_df, non_compliant_df]:
        data['Feedback'] = ''
        data['Checkbox'] = ''
        data['Review Date'] = ''
        data['Action Items'] = ''
        data['Priority'] = ''
        data['Remediation Status'] = ''

    # Create detailed analysis summaries
    service_summary = df.groupby('service').agg({
        'status': lambda x: (x == 'alarm').sum(),
        'project': 'nunique',
        'resource': 'count'
    }).rename(columns={
        'status': 'Issues Count',
        'project': 'Projects Affected',
        'resource': 'Total Resources'
    })

    # Initialize Excel writer with nan_inf_to_errors option
    with pd.ExcelWriter(final_report_file, engine='xlsxwriter') as writer:
        workbook = writer.book

        # Define formats
        formats = {
            'header': workbook.add_format({'bold': True, 'bg_color': '#FFA07A', 'font_color': 'black'}),
            'red': workbook.add_format({'bg_color': '#FF0000', 'font_color': 'white'}),
            'green': workbook.add_format({'bg_color': '#008000', 'font_color': 'white'}),
            'section_header_red': workbook.add_format({'bold': True, 'bg_color': '#FF0000', 'font_color': 'white', 'font_size': 12}),
            'section_header_green': workbook.add_format({'bold': True, 'bg_color': '#008000', 'font_color': 'white', 'font_size': 12}),
            'zebra_light': workbook.add_format({'bg_color': '#F0F0F0'}),
            'zebra_dark': workbook.add_format({'bg_color': '#E0E0E0'}),
            'green_header': workbook.add_format({'bold': True, 'bg_color': '#90EE90', 'font_color': 'black'}),
            'priority_red': workbook.add_format({'bg_color': '#FFB6C1', 'font_color': 'black'}),
            'priority_green': workbook.add_format({'bg_color': '#98FB98', 'font_color': 'black'})
        }

        # Write raw data sheet
        raw_df.to_excel(writer, sheet_name='Report_pp', index=False)
        raw_worksheet = writer.sheets['Report_pp']
        for col_num, value in enumerate(raw_df.columns.values):
            raw_worksheet.write(0, col_num, value, formats['header'])

        # Write consolidated sheet
        consolidated_sheet = workbook.add_worksheet('Consolidated')
        
        # Write non-compliant section
        consolidated_sheet.write(0, 0, 'Non-compliant Findings', formats['section_header_red'])
        headers = ['service', 'title', 'status', 'control_title', 'control_description', 
                  'reason', 'resource', 'project', 'location', 'Feedback', 'Checkbox', 
                  'Review Date', 'Action Items', 'Priority', 'Remediation Status']
        
        for col, header in enumerate(headers):
            consolidated_sheet.write(1, col, header, formats['header'])

        # Write non-compliant data with formatting and NaN handling
        for row_idx, row in enumerate(non_compliant_df.values, start=2):
            for col_idx, value in enumerate(row):
                # Handle NaN/INF values
                if isinstance(value, (float, np.floating)) and (pd.isna(value) or pd.isinf(value)):
                    value = ''
                
                if col_idx in [3, 4, 5, 6]:  # Format critical columns
                    consolidated_sheet.write(row_idx, col_idx, value, formats['red'])
                else:
                    consolidated_sheet.write(row_idx, col_idx, str(value))

        # Write compliant section
        compliant_start_row = len(non_compliant_df) + 4
        consolidated_sheet.write(compliant_start_row, 0, 'Compliant Findings', formats['section_header_green'])
        
        for col, header in enumerate(headers):
            consolidated_sheet.write(compliant_start_row + 1, col, header, formats['header'])

        # Write compliant data with formatting and NaN handling
        for row_idx, row in enumerate(compliant_df.values, start=compliant_start_row + 2):
            for col_idx, value in enumerate(row):
                # Handle NaN/INF values
                if isinstance(value, (float, np.floating)) and (pd.isna(value) or pd.isinf(value)):
                    value = ''
                
                if col_idx in [3, 4, 5, 6]:  # Format critical columns
                    consolidated_sheet.write(row_idx, col_idx, value, formats['green'])
                else:
                    consolidated_sheet.write(row_idx, col_idx, str(value))

        # Write service analysis sheet
        service_summary.to_excel(writer, sheet_name='Service Analysis')
        analysis_sheet = writer.sheets['Service Analysis']
        
        for col_num, value in enumerate(service_summary.columns):
            analysis_sheet.write(0, col_num, value, formats['header'])

    # Create Summary Table for non-compliant findings
        summary = non_compliant_df.groupby(['title', 'control_title', 'control_description']).agg({
            'resource': 'count',
            'project': 'nunique',
            'Priority': lambda x: x.iloc[0] if not x.empty else 'Priority Not Added Yet'
        }).reset_index()
        
        summary.columns = ['Title', 'Control Title', 'Control Description', 'Resources Affected', 'Projects Affected', 'Priority']
        
        # Write Summary Table
        summary.to_excel(writer, sheet_name='Summary Tables', index=False)
        summary_worksheet = writer.sheets['Summary Tables']
        
        # Write headers
        for col_num, value in enumerate(summary.columns):
            summary_worksheet.write(0, col_num, value, formats['header'])
        
        # Apply zebra striping to Summary Table
        for row_num in range(1, len(summary) + 1):
            row_format = formats['zebra_dark'] if row_num % 2 == 0 else formats['zebra_light']
            for col_num in range(len(summary.columns)):
                value = summary.iloc[row_num - 1, col_num]
                if col_num == len(summary.columns) - 1:  # Priority column
                    format_to_use = formats['priority_red'] if value == 'Priority Not Added Yet' else formats['priority_green']
                else:
                    format_to_use = row_format
                summary_worksheet.write(row_num, col_num, value, format_to_use)

        # Add Compliant Summary Table below with spacing
        start_row = len(summary) + 3  # Leave 2 rows gap
        
        # Create Compliant Summary
        compliant_summary = compliant_df.groupby(['title', 'control_title', 'control_description']).agg({
            'resource': 'count',
            'project': 'nunique'
        }).reset_index()
        
        compliant_summary.columns = ['Title', 'Control Title', 'Control Description', 'Resources Affected', 'Projects Affected']
        compliant_summary['Status'] = 'Safe/Well Architected'
        
        # Write section header
        summary_worksheet.write(start_row, 0, 'Compliant Findings Summary', formats['section_header_green'])
        
        # Write headers
        for col_num, value in enumerate(compliant_summary.columns):
            summary_worksheet.write(start_row + 1, col_num, value, formats['green_header'])
        
        # Apply zebra striping to Compliant Summary
        for row_num in range(len(compliant_summary)):
            row_format = formats['zebra_dark'] if row_num % 2 == 0 else formats['zebra_light']
            for col_num in range(len(compliant_summary.columns)):
                value = compliant_summary.iloc[row_num, col_num]
                summary_worksheet.write(row_num + start_row + 2, col_num, value, row_format)

        # Adjust column widths
        for worksheet in [summary_worksheet]:
            for col_num in range(len(compliant_summary.columns)):
                worksheet.set_column(col_num, col_num, 20)

    print(f"Enhanced report generated: {final_report_file}")

def main():
    """
    Main function to handle report generation.
    """
    try:
        report_file = input("Enter the GCP report file name: ").strip()
        if not os.path.exists(report_file):
            raise FileNotFoundError(f"File not found: {report_file}")
            
        base_name = os.path.splitext(os.path.basename(report_file))[0]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_file_name = f"{base_name}_enhanced_report_{timestamp}.xlsx"
        reports_directory = os.path.dirname(os.path.abspath(__file__))
        final_report_file = os.path.join(reports_directory, unique_file_name)

        create_simplified_gcp_report(report_file, final_report_file)
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
