import pandas as pd
from datetime import datetime
import os
import numpy as np

# Define service categories
categories = {
    'Security and Identity': ['IAM', 'ACM', 'KMS', 'GuardDuty', 'Secret Manager', 'Secret Hub', 'SSM'],
    'Compute': ['Auto Scaling', 'EC2', 'ECS', 'EKS', 'Lambda', 'EMR', 'Step Functions'],
    'Storage': ['EBS', 'ECR', 'S3', 'DLM', 'Backup'],
    'Network': ['API Gateway', 'CloudFront', 'Route 53', 'VPC', 'ELB', 'ElasticCache', 'CloudTrail'],
    'Database': ['RDS', 'DynamoDB', 'Athena', 'Glue'],
    'Other': ['CloudFormation', 'CodeDeploy', 'Config', 'SNS', 'SQS', 'WorkSpaces', 'EventBridge', 'Config']
}

def load_data(input_file, priority_file):
    if input_file.endswith(".xlsx"):
        df_input = pd.read_excel(input_file)
    elif input_file.endswith(".csv"):
        df_input = pd.read_csv(input_file, low_memory=False)
    else:
        raise ValueError("Unsupported file type")

    # Load priority database
    df_priority = pd.read_excel(priority_file)
    
    return df_input, df_priority

def update_priority_and_recommendation(df_input, df_priority):
    for idx, row in df_input.iterrows():
        control_title = row["control_title"]
        status = row["status"]

        matching_row = df_priority[df_priority["control_title"] == control_title]

        if not matching_row.empty:
            priority = matching_row.iloc[0]["priority"]
            recommendation = matching_row.iloc[0]["Recommendation Steps/Approach"]

            if status in ["ok", "info", "skip"]:
                df_input.at[idx, "priority"] = "Safe/Well Architected"
                df_input.at[idx, "Recommendation Steps/Approach"] = recommendation
                df_input.at[idx, "priority_color"] = "008000"  # Green
            else:
                df_input.at[idx, "priority"] = priority
                df_input.at[idx, "Recommendation Steps/Approach"] = recommendation
                
                if priority == "High":
                    df_input.at[idx, "priority_color"] = "FF0000"  # Red
                elif priority == "Medium":
                    df_input.at[idx, "priority_color"] = "FFA500"  # Orange
                elif priority == "Low":
                    df_input.at[idx, "priority_color"] = "FFFF00"  # Yellow
        else:
            df_input.at[idx, "priority"] = "No data"
            df_input.at[idx, "Recommendation Steps/Approach"] = "No recommendation available"
            df_input.at[idx, "priority_color"] = "FFFFFF"  # White

    return df_input

def create_enhanced_report(df_input, final_report_file):
    # Create Excel writer with nan_inf_to_errors option
    with pd.ExcelWriter(final_report_file, engine='xlsxwriter', engine_kwargs={'options': {'nan_inf_to_errors': True}}) as writer:
        workbook = writer.book

        # Define formats
        formats = {
            'header': workbook.add_format({'bold': True, 'bg_color': '#FFA07A', 'font_color': 'black'}),
            'red': workbook.add_format({'bg_color': '#FF0000', 'font_color': 'white'}),
            'orange': workbook.add_format({'bg_color': '#FFA500', 'font_color': 'black'}),
            'yellow': workbook.add_format({'bg_color': '#FFFF00', 'font_color': 'black'}),
            'green': workbook.add_format({'bg_color': '#008000', 'font_color': 'white'}),
            'section_header_red': workbook.add_format({'bold': True, 'bg_color': '#FF0000', 'font_color': 'white', 'font_size': 12}),
            'section_header_green': workbook.add_format({'bold': True, 'bg_color': '#008000', 'font_color': 'white', 'font_size': 12}),
            'zebra_light': workbook.add_format({'bg_color': '#F0F0F0'}),
            'zebra_dark': workbook.add_format({'bg_color': '#E0E0E0'})
        }

        # Create all necessary sheets first
        workbook.add_worksheet('Report_Raw.pp')
        workbook.add_worksheet('Summary Tables')
        workbook.add_worksheet('Category Analysis')
        workbook.add_worksheet('Consolidated')

        # Create category sheets
        for category in categories.keys():
            sheet_name = category.replace(' ', '_')[:31]
            workbook.add_worksheet(sheet_name)

        # Clean the dataframe before writing
        df_input_clean = df_input.fillna('')  # Replace NaN with empty string

        # Write raw data sheet
        df_input_clean.to_excel(writer, sheet_name='Report_Raw.pp', index=False)
        raw_sheet = writer.sheets['Report_Raw.pp']
        for col_num, value in enumerate(df_input_clean.columns.values):
            raw_sheet.write(0, col_num, value, formats['header'])

        # Create category sheets
        create_category_sheets(writer, df_input_clean, formats)

        # Create summary tables
        create_summary_tables(writer, df_input_clean, formats)

        # Create consolidated sheet
        create_consolidated_sheet(writer, df_input_clean, formats)

        # Create category summary
        create_category_summary_table(writer, df_input_clean, formats)

def safe_write(sheet, row, col, value, format):
    """Helper function to safely write values to Excel"""
    if pd.isna(value) or value is None:
        sheet.write(row, col, '', format)
    else:
        try:
            sheet.write(row, col, value, format)
        except Exception:
            sheet.write(row, col, str(value), format)

def write_consolidated_section(sheet, df, start_row, columns, formats, is_compliant):
    row = start_row
    for _, data_row in df.iterrows():
        for col, column in enumerate(columns):
            value = data_row[column]
            
            # Determine format based on column and compliance status
            if column in ['title', 'status']:
                format_to_use = formats['green'] if is_compliant else formats['red']
            elif column == 'priority':
                if is_compliant:
                    format_to_use = formats['green']
                    value = "Safe/Well Architected"
                else:
                    priority = data_row['priority']
                    format_to_use = formats['red'] if priority == 'High' else \
                                  formats['orange'] if priority == 'Medium' else \
                                  formats['yellow'] if priority == 'Low' else formats['zebra_light']
            else:
                format_to_use = formats['zebra_light']
            
            safe_write(sheet, row, col, value, format_to_use)
        row += 1
    
    return row

def write_summary_section(sheet, df, start_row, title, formats, is_compliant):
    # Write section header
    header_format = formats['section_header_green'] if is_compliant else formats['section_header_red']
    sheet.write(start_row, 0, title, header_format)
    
    # Write column headers
    headers = ['Title', 'Control Title', 'Control Description', 'Open Issues', 'Priority']
    for col, header in enumerate(headers):
        sheet.write(start_row + 1, col, header, formats['header'])
    
    # Prepare and write data
    summary = df.groupby(['title', 'control_title', 'control_description']).size().reset_index(name='Open Issues')
    
    for row_idx, row in summary.iterrows():
        actual_row = start_row + row_idx + 2
        row_format = formats['zebra_dark'] if row_idx % 2 == 0 else formats['zebra_light']
        
        safe_write(sheet, actual_row, 0, row['title'], row_format)
        safe_write(sheet, actual_row, 1, row['control_title'], row_format)
        safe_write(sheet, actual_row, 2, row['control_description'], row_format)
        safe_write(sheet, actual_row, 3, row['Open Issues'], row_format)
        
        # Write priority with appropriate formatting
        if is_compliant:
            sheet.write(actual_row, 4, "Safe/Well Architected", formats['green'])
        else:
            priority = df[df['control_title'] == row['control_title']]['priority'].iloc[0]
            format_to_use = formats['red'] if priority == 'High' else \
                           formats['orange'] if priority == 'Medium' else \
                           formats['yellow'] if priority == 'Low' else row_format
            safe_write(sheet, actual_row, 4, priority, format_to_use)

def create_summary_tables(writer, df, formats):
    summary_sheet = writer.sheets['Summary Tables']
    
    # Set column widths
    column_widths = {'Title': 25, 'Control Title': 40, 'Control Description': 60, 'Open Issues': 15, 'Priority': 20}
    for col, width in enumerate(column_widths.values()):
        summary_sheet.set_column(col, col, width)

    # Non-compliant findings section
    non_compliant_df = df[df['status'] == 'alarm']
    write_summary_section(summary_sheet, non_compliant_df, 0, "Non-Compliant Findings", formats, is_compliant=False)

    # Calculate the last row of non-compliant section
    last_row = len(non_compliant_df) + 3  # Header + title + data rows

    # Compliant findings section
    compliant_df = df[df['status'].isin(['ok', 'info', 'skip'])]
    write_summary_section(summary_sheet, compliant_df, last_row + 2, "Compliant Findings", formats, is_compliant=True)

def write_summary_section(sheet, df, start_row, title, formats, is_compliant):
    # Write section header
    header_format = formats['section_header_green'] if is_compliant else formats['section_header_red']
    sheet.write(start_row, 0, title, header_format)
    
    # Write column headers
    headers = ['Title', 'Control Title', 'Control Description', 'Open Issues', 'Priority']
    for col, header in enumerate(headers):
        sheet.write(start_row + 1, col, header, formats['header'])
    
    # Prepare and write data
    summary = df.groupby(['title', 'control_title', 'control_description']).size().reset_index(name='Open Issues')
    
    for row_idx, row in summary.iterrows():
        actual_row = start_row + row_idx + 2
        row_format = formats['zebra_dark'] if row_idx % 2 == 0 else formats['zebra_light']
        
        sheet.write(actual_row, 0, row['title'], row_format)
        sheet.write(actual_row, 1, row['control_title'], row_format)
        sheet.write(actual_row, 2, row['control_description'], row_format)
        sheet.write(actual_row, 3, row['Open Issues'], row_format)
        
        # Write priority with appropriate formatting
        if is_compliant:
            sheet.write(actual_row, 4, "Safe/Well Architected", formats['green'])
        else:
            priority = df[df['control_title'] == row['control_title']]['priority'].iloc[0]
            format_to_use = formats['red'] if priority == 'High' else \
                           formats['orange'] if priority == 'Medium' else \
                           formats['yellow'] if priority == 'Low' else row_format
            sheet.write(actual_row, 4, priority, format_to_use)

def create_consolidated_sheet(writer, df, formats):
    consolidated_sheet = writer.sheets['Consolidated']
    
    # Define columns to show
    columns = ['title', 'status', 'control_title', 'control_description', 
              'Recommendation Steps/Approach', 'region', 'account_id', 
              'resource', 'reason', 'priority']
    
    # Set column widths
    column_widths = {
        'title': 25, 'status': 15, 'control_title': 40, 
        'control_description': 60, 'Recommendation Steps/Approach': 60,
        'region': 15, 'account_id': 20, 'resource': 40, 
        'reason': 50, 'priority': 20
    }
    
    for col, column in enumerate(columns):
        consolidated_sheet.set_column(col, col, column_widths.get(column, 15))
    
    # Write headers
    for col, column in enumerate(columns):
        consolidated_sheet.write(0, col, column, formats['header'])
    
    # Process non-compliant findings (alarm status)
    alarm_df = df[df['status'] == 'alarm']
    row = 1
    row = write_consolidated_section(consolidated_sheet, alarm_df, row, columns, formats, is_compliant=False)
    
    # Add a blank row
    row += 1
    
    # Process compliant findings (ok, info, skip status)
    compliant_df = df[df['status'].isin(['ok', 'info', 'skip'])]
    write_consolidated_section(consolidated_sheet, compliant_df, row, columns, formats, is_compliant=True)

def write_consolidated_section(sheet, df, start_row, columns, formats, is_compliant):
    row = start_row
    for _, data_row in df.iterrows():
        for col, column in enumerate(columns):
            value = data_row[column]
            
            # Determine format based on column and compliance status
            if column in ['title', 'status']:
                format_to_use = formats['green'] if is_compliant else formats['red']
            elif column == 'priority':
                if is_compliant:
                    format_to_use = formats['green']
                    value = "Safe/Well Architected"
                else:
                    priority = data_row['priority']
                    format_to_use = formats['red'] if priority == 'High' else \
                                  formats['orange'] if priority == 'Medium' else \
                                  formats['yellow'] if priority == 'Low' else formats['zebra_light']
            else:
                format_to_use = formats['zebra_light']
            
            sheet.write(row, col, value, format_to_use)
        row += 1
    
    return row

def create_category_sheets(writer, df, formats):
    category_columns = [
        'title', 'control_title', 'control_description', 
        'Recommendation Steps/Approach', 'region', 'account_id', 
        'resource', 'reason', 'priority', 'Feedback', 
        'Checkbox', 'Review Date', 'Action Items'
    ]

    df['Feedback'] = ''
    df['Checkbox'] = ''
    df['Review Date'] = ''
    df['Action Items'] = ''

    for category, services in categories.items():
        category_data = df[df['title'].isin(services)]
        if not category_data.empty:
            category_data = category_data[category_columns]
            
            sheet_name = category.replace(' ', '_')[:31]
            category_data.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            
            # Format headers and set column widths
            for col_num, value in enumerate(category_data.columns.values):
                worksheet.write(0, col_num, value, formats['header'])
                worksheet.set_column(col_num, col_num, 20)  # Set standard width

            # Apply priority color formatting
            priority_col = category_columns.index('priority')
            for row_num, priority in enumerate(category_data['priority'], start=1):
                if priority == 'High':
                    worksheet.write(row_num, priority_col, priority, formats['red'])
                elif priority == 'Medium':
                    worksheet.write(row_num, priority_col, priority, formats['orange'])
                elif priority == 'Low':
                    worksheet.write(row_num, priority_col, priority, formats['yellow'])
                elif priority == 'Safe/Well Architected':
                    worksheet.write(row_num, priority_col, priority, formats['green'])

def create_category_summary_table(writer, df, formats):
    category_sheet = writer.sheets['Category Analysis']
    
    # Set column widths
    column_widths = {'Category': 25, 'Open Issues': 15, 'Safe Count': 15, 'Total': 15}
    for col, width in enumerate(column_widths.values()):
        category_sheet.set_column(col, col, width)
    
    # Write headers
    headers = ['Category', 'Open Issues', 'Safe Count', 'Total']
    for col, header in enumerate(headers):
        category_sheet.write(0, col, header, formats['header'])
    
    row = 1
    for category, services in categories.items():
        category_data = df[df['title'].isin(services)]
        if not category_data.empty:
            open_issues = len(category_data[category_data['status'] == 'alarm'])
            safe_count = len(category_data[category_data['status'].isin(['ok', 'info', 'skip'])])
            total = open_issues + safe_count
            
            category_sheet.write(row, 0, category, formats['zebra_light'])
            category_sheet.write(row, 1, open_issues, formats['red'])
            category_sheet.write(row, 2, safe_count, formats['green'])
            category_sheet.write(row, 3, total, formats['zebra_light'])
            row += 1

def main():
    try:
        input_file = input("Enter the input file name (CSV or Excel): ")
        priority_file = "PowerPipeControls_Annotations.xlsx"
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.splitext(input_file)[0]
        output_file = f"{filename}_PowerPipe_Report_{timestamp}.xlsx"

        print("\nLoading data files...")
        df_input, df_priority = load_data(input_file, priority_file)
        
        print("Updating priority and recommendations...")
        updated_df = update_priority_and_recommendation(df_input, df_priority)
        
        print("Generating enhanced report...")
        create_enhanced_report(updated_df, output_file)
        
        print(f"\nEnhanced report generated successfully: {output_file}")
        
    except FileNotFoundError as e:
        print(f"\nError: File not found - {str(e)}")
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
