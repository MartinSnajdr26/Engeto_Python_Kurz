import pandas as pd
import tkinter as tk
from tkinter import filedialog
import re  # Import the regular expressions library

# Initialize global variables for file paths
input_path = ''
output_path = ''
second_input_path = ''

# Function to select the input Excel file path
def select_input_path():
    global input_path
    input_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    input_label.config(text="Input File: " + input_path)

# Function to select the output Excel file path
def select_output_path():
    global output_path
    output_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx;*.xls")])
    output_label.config(text="Output File: " + output_path)

# Function to select the second input Excel file path
def select_second_input_path():
    global second_input_path
    second_input_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    second_input_label.config(text="Second Input File: " + second_input_path)

# Function to clean 'Name of Credit Rep' by removing codes in parentheses or brackets
def clean_name(name):
    name = str(name)  # Convert 'name' to string to avoid errors
    return re.sub(r"[\(\[].*?[\)\]]", "", name).strip()  # Use regex to remove text within parentheses or brackets

# Function to process the Excel file and select accounts
def process_excel():
    if not input_path or not output_path:
        result_label.config(text="Please select both input and output paths.")
        return

    try:
        df = pd.read_excel(input_path)  # Read the input Excel file into a DataFrame
        df['Name of Credit Rep'] = df['Name of Credit Rep'].apply(clean_name)  # Clean up the 'Name of Credit Rep' column

        # Filter out the rows where 'Total Blocked Orders' is 0
        df = df[df['Total Blocked Orders'] > 0]

        # Group by the cleaned 'Name of Credit Rep'
        grouped = df.groupby('Name of Credit Rep')
        selected_accounts = pd.DataFrame()

        for name, group in grouped:
            if group.empty or len(group) < 2:  # Ensure the group has at least one account
                continue

            # Sort by 'Total Blocked Orders', descending
            sorted_group = group.sort_values(by='Total Blocked Orders', ascending=False)

            # Select the account with the highest 'Total Blocked Orders'
            top_blocked_order = sorted_group.iloc[0]

            # Attempt to select the account with the highest 'Sum of Credit Limit' that's not the same as 'top_blocked_order'
            sorted_group_non_zero_credit = sorted_group[sorted_group['Sum of Credit Limit'] > 0]
            if not sorted_group_non_zero_credit.empty and len(sorted_group_non_zero_credit) > 1:
                top_credit_limit = sorted_group_non_zero_credit.sort_values(by='Sum of Credit Limit', ascending=False).iloc[0]
            else:
                # If there's no non-zero credit limit or only one account, take the second 'Total Blocked Orders'
                top_credit_limit = sorted_group.iloc[1] if len(sorted_group) > 1 and sorted_group.iloc[1]['Credit Acc number'] != top_blocked_order['Credit Acc number'] else None
                if top_credit_limit is not None:
                    selected_accounts = pd.concat([selected_accounts, top_credit_limit.to_frame().T])

            # Append the selected accounts to the selected_accounts DataFrame
            selected_accounts = pd.concat([selected_accounts, top_blocked_order.to_frame().T])

        selected_accounts.drop_duplicates(subset='Credit Acc number', keep='first', inplace=True)  # Remove duplicate accounts
        selected_accounts.to_excel(output_path, index=False)  # Save the selected accounts to the output Excel file
        result_label.config(text="First selection complete! Output saved to: " + output_path)

        process_second_excel(selected_accounts)  # Call the function to process the second Excel file

    except Exception as e:
        result_label.config(text="An error occurred: " + str(e))

# Function to process the second Excel file and select random orders
def process_second_excel(selected_accounts):
    if not second_input_path:
        result_label.config(text="Please select the second input path.")
        return

    try:
        second_df = pd.read_excel(second_input_path)
        
        # Ensure 'Credit Acc number' is of the same type in both DataFrames
        second_df['Credit Acc number'] = second_df['Credit Acc number'].astype(str)
        selected_accounts['Credit Acc number'] = selected_accounts['Credit Acc number'].astype(str)

        # Filter the second DataFrame based on the 'Credit Acc number' from selected_accounts
        filtered_orders = second_df[second_df['Credit Acc number'].isin(selected_accounts['Credit Acc number'])]

        # Select a random order for each 'Credit Acc number'
        orders_to_output = filtered_orders.groupby('Credit Acc number').apply(lambda x: x.sample(1)).reset_index(drop=True)

        # Write the results to a new sheet in the same output Excel file
        with pd.ExcelWriter(output_path, mode='a', if_sheet_exists='new') as writer:
            orders_to_output.to_excel(writer, sheet_name='Random Selected Orders', index=False)
            result_label.config(text="Random selection complete! Output saved to new sheet in: " + output_path)
    except Exception as e:
        result_label.config(text="An error occurred in processing the second file: " + str(e))

# Set up the main application window
root = tk.Tk()
root.title("Account Selector")

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

# Second input file selection label and button
second_input_label = tk.Label(root, text="Select second input Excel file:")
second_input_label.pack()
second_input_button = tk.Button(root, text="Browse", command=select_second_input_path)
second_input_button.pack()

# Result label to display messages
result_label = tk.Label(root, text="")
result_label.pack()

# Process button to start the Excel processing
process_button = tk.Button(root, text="Process Files", command=process_excel)
process_button.pack()

# Run the main loop
root.mainloop()
