import pandas as pd
import re
import os
import tkinter as tk
from tkinter import filedialog

# Function to select the input Excel file path
def select_input_path():
    global input_path
    input_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    input_label.config(text=input_path)

# Function to select the output Excel file path
def select_output_path():
    global output_path
    output_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx;*.xls")])
    output_label.config(text=output_path)

# Function to process the Excel file
def process_excel():
    if not input_path or not output_path:
        result_label.config(text="Please select both input and output paths.")
        return

    if not os.access(input_path, os.R_OK):
        result_label.config(text=f"Cannot read the file at {input_path}. Please check the file permissions or if it's open in another program.")
        return

    try:
        df = pd.read_excel(input_path)
        # Filter out unwanted senders and subjects
        filtered_df = df[
            ~df['Sender'].str.contains('@medtronic.com', case=False, na=False) &
            ~df['Sender'].str.contains('no-reply@', case=False, na=False) &
            ~df['Subject'].str.contains('Auto', case=False, na=False)
        ]
        # Extract numbers from 'Subject' and filter out rows without numbers
        filtered_df.loc[:, 'Extracted_Number'] = filtered_df['Subject'].apply(lambda x: re.findall(r'\b\d{7}\b', str(x)))
        filtered_df = filtered_df[filtered_df['Extracted_Number'].apply(len) > 0]
        filtered_df.loc[:, 'Extracted_Number'] = filtered_df['Extracted_Number'].apply(lambda x: ', '.join(map(str, x)))

        # Filter for 'Done within of SLA' and 'Done outside of SLA'
        within_sla = filtered_df[filtered_df['SLA Category'] == 'Done within of SLA']
        outside_sla = filtered_df[filtered_df['SLA Category'] == 'Done outside of SLA']

        # Check if there are records in both categories
        if within_sla.empty or outside_sla.empty:
            result_label.config(text="Not enough records in one or both SLA categories.")
            return

        # Select unique records ensuring different senders for each user
        def select_unique_records(df):
            return df.drop_duplicates(subset=['User', 'Sender']).groupby('User').head(1)

        # Combine the two DataFrames, ensuring one record from each category per user
        combined_df = pd.concat([
            select_unique_records(within_sla),
            select_unique_records(outside_sla)
        ])

        # Remove duplicate subjects and senders for each user
        combined_df = combined_df.drop_duplicates(subset=['User', 'Subject'])
        combined_df = combined_df.drop_duplicates(subset=['User', 'Sender'])

        # Ensure at least two records per user with unique subjects and senders
        if combined_df.groupby('User').size().min() < 2:
            additional_records = filtered_df[~filtered_df.index.isin(combined_df.index)]
            for user, count in combined_df.groupby('User').size().items():
                if count < 2:
                    user_additional_records = select_unique_records(additional_records[additional_records['User'] == user])
                    user_additional_records = user_additional_records[
                        ~user_additional_records['Subject'].isin(combined_df[combined_df['User'] == user]['Subject'])
                    ]
                    user_additional_records = user_additional_records[
                        ~user_additional_records['Sender'].isin(combined_df[combined_df['User'] == user]['Sender'])
                    ]
                    combined_df = pd.concat([combined_df, user_additional_records.head(2 - count)])

        # Reset index after concatenation
        output_df = combined_df.reset_index(drop=True)

        output_df.to_excel(output_path, index=False)
        result_label.config(text=f"Output written to {output_path}")
        print("The Excel file has been processed and the output is saved successfully.")
    except Exception as e:
        result_label.config(text=f"An error occurred: {e}")

# Set up the main application window
root = tk.Tk()
root.title("Excel Processor")

# Input file selection label and button
input_label = tk.Label(root, text="Select input Excel file:")
input_label.pack()
input_button = tk.Button(root, text="Browse", command=select_input_path)
input_button.pack()

# Output file selection label and button
output_label = tk.Label(root, text="Select output Excel file:")
output_label.pack()
output_button = tk.Button(root, text="Browse", command=select_output_path)
output_button.pack()

# Process button to start processing the Excel file
process_button = tk.Button(root, text="Process", command=process_excel)
process_button.pack()

# Label to display results or errors
result_label = tk.Label(root, text="")
result_label.pack()

# Run the application
root.mainloop()
