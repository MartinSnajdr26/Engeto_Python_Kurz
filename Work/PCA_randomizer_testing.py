import pandas as pd
from openpyxl import Workbook
from tkinter import Tk, filedialog, Button, Label, Entry

class PCAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PCA Randomizer")
        
        # Initialize file paths
        self.input_file_path_1 = ""
        self.input_file_path_2 = ""
        self.output_file_path = ""
        
        # Set up the user interface
        self.setup_ui()
    
    def setup_ui(self):
        # Create and pack the UI components
        Label(self.root, text="PCA Randomizer").pack()
        
        Button(self.root, text="Select Recon Ratio Data Excel File", command=self.select_input_file_1).pack()
        Label(self.root, text="Sheet name for Recon Ratio Data:").pack()
        self.sheet_name_entry_1 = Entry(self.root)
        self.sheet_name_entry_1.insert(0, "Customer_View")
        self.sheet_name_entry_1.pack()
        
        Button(self.root, text="Select QC_PCA_Results Excel File", command=self.select_input_file_2).pack()
        Label(self.root, text="Sheet name for QC_PCA_Results:").pack()
        self.sheet_name_entry_2 = Entry(self.root)
        self.sheet_name_entry_2.insert(0, "QC_PCA")
        self.sheet_name_entry_2.pack()
        
        Button(self.root, text="Select Output File Location", command=self.select_output_file).pack()
        Button(self.root, text="Run", command=self.run).pack()
    
    def select_input_file_1(self):
        # Open file dialog to select the first input file
        self.input_file_path_1 = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        print(f"Selected Recon Ratio Data file: {self.input_file_path_1}")
    
    def select_input_file_2(self):
        # Open file dialog to select the second input file
        self.input_file_path_2 = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        print(f"Selected QC_PCA_Results file: {self.input_file_path_2}")
    
    def select_output_file(self):
        # Open file dialog to select the output file location
        self.output_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx *.xls")])
        print(f"Selected output file: {self.output_file_path}")
    
    def clean_group_name(self, name):
        # Clean the group name by removing text within parentheses or brackets
        if '(' in name:
            name = name.split('(')[0]
        elif '[' in name:
            name = name.split('[')[0]
        return name.strip()
    
    def load_excel(self, file_path, sheet_name):
        # Load an Excel file and return the specified sheet as a DataFrame
        excel_file = pd.ExcelFile(file_path)
        print(f"Available sheet names in {file_path}: {excel_file.sheet_names}")
        if sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            # Convert 'Created' column to datetime if it exists
            if 'Created' in df.columns:
                df['Created'] = pd.to_datetime(df['Created'])
            print(f"Columns in {sheet_name}: {df.columns.tolist()}")
            return df
        else:
            raise ValueError(f"Worksheet named '{sheet_name}' not found in {file_path}")
    
    def run(self):
        # Ensure all file paths are selected
        if not self.input_file_path_1 or not self.input_file_path_2 or not self.output_file_path:
            print("Please select both input files and output file location.")
            return
        
        # Get sheet names from user input
        sheet_name_1 = self.sheet_name_entry_1.get()
        sheet_name_2 = self.sheet_name_entry_2.get()

        try:
            # Load the Excel files
            df1 = self.load_excel(self.input_file_path_1, sheet_name_1)
            df2 = self.load_excel(self.input_file_path_2, sheet_name_2)
        except ValueError as e:
            print(e)
            return

        # Check for required columns in the first DataFrame
        if 'Country' not in df1.columns:
            print(f"'Country' column not found in {sheet_name_1}. Please check the input file.")
            return

        # Clean and preprocess data
        df1['Credit Representative Group Name'] = df1['Credit Representative Group Name'].apply(self.clean_group_name)
        df1['Customer Identifier'] = df1['Customer Identifier'].astype(str).str.lstrip('0')

        df2 = df2[df2['Title'] == 'PCA']
        df2['Account Number'] = df2['Account Number'].astype(str)

        # Merge DataFrames on 'Customer Identifier' and 'Account Number'
        merged_df = df1.merge(df2, left_on='Customer Identifier', right_on='Account Number', how='left')
        merged_df['Country'] = merged_df['Country_x'].combine_first(merged_df['Country_y'])
        
        merged_df['PCA_Result'] = merged_df['PCA_Result'].astype(str).fillna('Account not Audited')

        # Filter and process the merged DataFrame
        filtered_df = merged_df[
            (merged_df['Recon period'] != 'Not Required') & 
            ((merged_df['PCA_Result'] == 'Account not Audited') | (merged_df['PCA_Result'].astype(float) < 0.85))
        ]

        filtered_df = filtered_df.drop_duplicates(subset=['Customer Identifier', 'Credit Representative Group Name'])
        final_df = filtered_df.groupby('Credit Representative Group Name').apply(lambda x: x.nlargest(2, 'Total score')).reset_index(drop=True)

        # Combine information into a single column
        final_df['Combined Info'] = final_df.apply(
            lambda row: f"The customer total score is {row['Total score']} which means recon period is {row['Recon period']} and last PCA_Result was {row['PCA_Result']}.", 
            axis=1
        )

        # Prepare the output DataFrame
        output_df = final_df[['Title', 'Credit Representative Group Name', 'Customer Identifier', 'Country', 'Combined Info']]
        output_df = output_df.rename(columns={
            'Credit Representative Group Name': 'Collector',
            'Customer Identifier': 'Account Number',
            'Combined Info': 'PCA_4_Comment'
        })

        # Save the output DataFrame to an Excel file
        output_df.to_excel(self.output_file_path, index=False)
        print(f"Output saved to {self.output_file_path}")

if __name__ == "__main__":
    root = Tk()
    app = PCAApp(root)
    root.mainloop()
