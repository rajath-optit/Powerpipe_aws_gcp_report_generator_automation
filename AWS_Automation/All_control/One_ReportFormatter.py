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
    # Create Excel writer
    with pd.ExcelWriter(final_report_file, engine='xlsxwriter') as writer:
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

        # First write the raw data sheet
        df_input.to_excel(writer, sheet_name='Report_Raw.pp', index=False)
        raw_sheet = writer.sheets['Report_Raw.pp']
        for col_num, value in enumerate(df_input.columns.values):
            raw_sheet.write(0, col_num, value, formats['header'])

        # Create category sheets with specific columns
        create_category_sheets(writer, df_input, formats)

        # Create summary tables last
        create_summary_tables(writer, df_input, formats)

def create_category_sheets(writer, df, formats):
    # Define columns for category sheets
    category_columns = [
        'title', 'control_title', 'control_description', 
        'Recommendation Steps/Approach', 'region', 'account_id', 
        'resource', 'reason', 'priority', 'Feedback', 
        'Checkbox', 'Review Date', 'Action Items'
    ]

    # Add empty columns for engineer input
    df['Feedback'] = ''
    df['Checkbox'] = ''
    df['Review Date'] = ''
    df['Action Items'] = ''

    for category, services in categories.items():
        category_data = df[df['title'].isin(services)]
        if not category_data.empty:
            # Select and reorder columns
            category_data = category_data[category_columns]
            
            # Write to sheet
            sheet_name = category.replace(' ', '_')[:31]  # Excel sheet name length limit
            category_data.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            
            # Format headers
            for col_num, value in enumerate(category_data.columns.values):
                worksheet.write(0, col_num, value, formats['header'])
                worksheet.set_column(col_num, col_num, 15)

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

def create_summary_tables(writer, df, formats):
    workbook = writer.book
    summary_sheet = workbook.add_worksheet('Summary Tables')
    
    # Non-compliant findings summary
    non_compliant_df = df[df['status'] == 'alarm']
    summary = non_compliant_df.groupby(['title', 'control_title', 'control_description', 'priority']).size().reset_index(name='Open Issues')
    
    # Write non-compliant section header
    summary_sheet.write(0, 0, 'Non-Compliant Findings', formats['section_header_red'])
    
    # Write headers in specified order
    headers = ['Title', 'Control Title', 'Control Description', 'Open Issues', 'Priority']
    for col, header in enumerate(headers):
        summary_sheet.write(1, col, header, formats['header'])
    
    # Write data with formatting
    for row_idx, row in summary.iterrows():
        row_format = formats['zebra_dark'] if row_idx % 2 == 0 else formats['zebra_light']
        
        # Write Title, Control Title, Control Description
        summary_sheet.write(row_idx + 2, 0, row['title'], row_format)
        summary_sheet.write(row_idx + 2, 1, row['control_title'], row_format)
        summary_sheet.write(row_idx + 2, 2, row['control_description'], row_format)
        summary_sheet.write(row_idx + 2, 3, row['Open Issues'], row_format)
        
        # Format priority column with color
        priority = row['priority']
        if priority == 'High':
            format_to_use = formats['red']
        elif priority == 'Medium':
            format_to_use = formats['orange']
        elif priority == 'Low':
            format_to_use = formats['yellow']
        else:
            format_to_use = row_format
        summary_sheet.write(row_idx + 2, 4, priority, format_to_use)
    
    # Add category summary at the end
    create_category_summary_table(writer, df, formats)

def create_category_summary_table(writer, df, formats):
    category_sheet = writer.book.add_worksheet('Category Analysis')
    
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
    input_file = input("Enter the input file name (CSV or Excel): ")
    priority_file = "PowerPipeControls_Annotations.xlsx"
    
    # Create unique timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.splitext(input_file)[0]
    output_file = f"{filename}_PowerPipe_Report_{timestamp}.xlsx"

    # Load and process data
    df_input, df_priority = load_data(input_file, priority_file)
    updated_df = update_priority_and_recommendation(df_input, df_priority)
    create_enhanced_report(updated_df, output_file)
    
    print(f"\nEnhanced report generated: {output_file}")

if __name__ == "__main__":
    main()
