import pandas as pd
import openpyxl
from openpyxl import Workbook
from tkinter import Tk, filedialog, Button, Label, Entry

class PCAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PCA Randomizer")
        
        self.input_file_path_1 = ""
        self.input_file_path_2 = ""
        self.output_file_path = ""
        
        self.label = Label(root, text="PCA Randomizer")
        self.label.pack()
        
        self.select_input_button_1 = Button(root, text="Select Recon Ratio Data Excel File", command=self.select_input_file_1)
        self.select_input_button_1.pack()
        
        self.sheet_name_label_1 = Label(root, text="Sheet name for Recon Ratio Data:")
        self.sheet_name_label_1.pack()
        self.sheet_name_entry_1 = Entry(root)
        self.sheet_name_entry_1.insert(0, "Customer_View")  # default value
        self.sheet_name_entry_1.pack()
        
        self.select_input_button_2 = Button(root, text="Select QC_PCA_Results Excel File", command=self.select_input_file_2)
        self.select_input_button_2.pack()
        
        self.sheet_name_label_2 = Label(root, text="Sheet name for QC_PCA_Results:")
        self.sheet_name_label_2.pack()
        self.sheet_name_entry_2 = Entry(root)
        self.sheet_name_entry_2.insert(0, "QC_PCA")  # default value
        self.sheet_name_entry_2.pack()
        
        self.select_output_button = Button(root, text="Select Output File Location", command=self.select_output_file)
        self.select_output_button.pack()
        
        self.run_button = Button(root, text="Run", command=self.run)
        self.run_button.pack()
    
    def select_input_file_1(self):
        self.input_file_path_1 = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        print(f"Selected Recon Ratio Data file: {self.input_file_path_1}")
    
    def select_input_file_2(self):
        self.input_file_path_2 = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        print(f"Selected QC_PCA_Results file: {self.input_file_path_2}")
    
    def select_output_file(self):
        self.output_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx *.xls")])
        print(f"Selected output file: {self.output_file_path}")
    
    def clean_group_name(self, name):
        if '(' in name:
            name = name.split('(')[0]
        elif '[' in name:
            name = name.split('[')[0]
        return name.strip()
    
    def load_excel(self, file_path, sheet_name):
        excel_file = pd.ExcelFile(file_path)
        print(f"Available sheet names in {file_path}: {excel_file.sheet_names}")
        if sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            if 'Created' in df.columns:
                df['Created'] = pd.to_datetime(df['Created'])
            print(f"Columns in {sheet_name}: {df.columns.tolist()}")
            return df
        else:
            raise ValueError(f"Worksheet named '{sheet_name}' not found in {file_path}")
    
    def run(self):
        if not self.input_file_path_1 or not self.input_file_path_2 or not self.output_file_path:
            print("Please select both input files and output file location.")
            return
        
        sheet_name_1 = self.sheet_name_entry_1.get()
        sheet_name_2 = self.sheet_name_entry_2.get()

        # Load the first Excel file into a DataFrame
        df1 = self.load_excel(self.input_file_path_1, sheet_name_1)
        
        # Clean the Credit Representative Group Name in the first DataFrame
        df1['Credit Representative Group Name'] = df1['Credit Representative Group Name'].apply(self.clean_group_name)
        
        # Remove leading zeros from the 'Customer Identifier' column in df1
        df1['Customer Identifier'] = df1['Customer Identifier'].astype(str).str.lstrip('0')
        
        # Load the second Excel file into a DataFrame
        df2 = self.load_excel(self.input_file_path_2, sheet_name_2)
        
        # Filter df2 to only include rows where 'Title' is 'PCA'
        df2 = df2[df2['Title'] == 'PCA']
        
        # Ensure the 'Account Number' in df2 is also a string
        df2['Account Number'] = df2['Account Number'].astype(str)
        
        # Debugging: print the column names of both dataframes to ensure we are using the correct column names
        print(f"Columns in Recon Ratio Data (df1): {df1.columns.tolist()}")
        print(f"Columns in QC_PCA_Results (df2): {df2.columns.tolist()}")
        
        # Merge the dataframes based on the selection criteria
        merged_df = df1.merge(df2, left_on='Customer Identifier', right_on='Account Number', how='left')  # Use left join to include all df1
        
        # Add "Account not Audited" message to rows where PCA_Result is missing
        merged_df['PCA_Result'] = merged_df['PCA_Result'].astype(str).fillna('Account not Audited')
        
        # Filter based on the criteria including the latest month
        filtered_df = merged_df[(merged_df['Recon period'] != 'Not Required') & ((merged_df['PCA_Result'] == 'Account not Audited') | (merged_df['PCA_Result'].astype(float) < 0.85))]
        
        # Drop duplicates based on 'Customer Identifier' and 'Credit Representative Group Name'
        filtered_df = filtered_df.drop_duplicates(subset=['Customer Identifier', 'Credit Representative Group Name'])
        
        # Select top 2 accounts per Credit Representative Group Name based on Total score
        final_df = filtered_df.groupby('Credit Representative Group Name').apply(lambda x: x.nlargest(2, 'Total score')).reset_index(drop=True)
        
        # Select relevant columns
        output_df = final_df[['Credit Representative Group Name', 'Company Code', 'Customer Identifier', 'Customer Name', 'DB Volume', 'CR Volume', 'DB $', 'CR $', 'Revenue', 'Total score', 'Recon period', 'PCA_Result', 'Created']]
        
        # Save the output to the specified output file
        output_df.to_excel(self.output_file_path, index=False)
        
        print(f"Output saved to {self.output_file_path}")

if __name__ == "__main__":
    root = Tk()
    app = PCAApp(root)
    root.mainloop()
