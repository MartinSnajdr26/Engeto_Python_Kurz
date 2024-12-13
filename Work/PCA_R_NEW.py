import pandas as pd

# Hardcoded list of agents
agents = [
    "Alp, Filip",
    "Antoniuk, Taras",
    "Arpitha, J",
    "Bagirov, Kyamran",
    "Cebola, Cristiano",
    "Czarnecka, Monika",
    "Dias, Alberto",
    "Dimitrewska, Agata",
    "Fourneret, Monika",
    "Gogula, Marina",
    "Grzybowska Dominika",
    "Grzybowska, Dominika",
    "Guminska, Julia",
    "Hagen, Marta",
    "Hamilton, Philip",
    "Harshitha Chandrashek",
    "Hentunen, Teemu",
    "Himadri Roy",
    "Knap, Weronika",
    "Kolesko, Magda",
    "Kott, Sara",
    "Krasucka, Karolina",
    "Krucz, Malgorzata",
    "Lal, Patrycja",
    "MB, Rashmi",
    "Mohammed Hussain Khan",
    "Mzyk, Sebastian",
    "Nanjunda, Harini",
    "Nedjar, Mouloud",
    "Okoumba, Ange",
    "Paradowski, Rafal",
    "Potrzebska, Karolina",
    "Raczynska, Alicja",
    "Rogala, Agata",
    "Sobanski, Ibolya",
    "Sokolowska, Paulina",
    "Spandana Ambati",
    "Sulkowska, Agnieszka",
    "Sum, Maria",
    "Sunil Dharamchand",
    "Szostak, Agnieszka",
    "Szymanek, Joanna",
    "Szymanska, Katarzyna",
    "Urbanska, Carla",
    "Viougeas, Kayetan",
    "Vlnova, Lucie"
]

# Load the Excel file and specify the sheet name
file_path = r'C:\Users\snajdm2\OneDrive - Medtronic PLC\PCA_P06.xlsx'
df = pd.read_excel(file_path, sheet_name='all data')

# Debugging: Print the first few rows of the DataFrame
print("First few rows of the DataFrame:")
print(df.head())

# Function to select up to 2 unique customer identifiers per tier for each agent
def select_customers(df):
    selected_customers = pd.DataFrame(columns=df.columns)
    
    for agent in agents:
        agent_df = df[df['Agent'].str.strip() == agent.strip()]
        
        # Debugging: Print the number of rows for the current agent
        print(f"Agent: {agent}, Number of rows: {len(agent_df)}")
        
        # Split the data by tiers
        tier_a = agent_df[agent_df['Tier'].str.strip() == 'Tier A']
        tier_b = agent_df[agent_df['Tier'].str.strip() == 'Tier B']
        tier_c = agent_df[agent_df['Tier'].str.strip() == 'Tier C']
        
        # Debugging: Print the number of rows for each tier
        print(f"Tier A: {len(tier_a)} rows")
        print(f"Tier B: {len(tier_b)} rows")
        print(f"Tier C: {len(tier_c)} rows")
        
        # Randomly select up to 2 customers from each tier
        selected_a = tier_a.sample(n=2) if len(tier_a) >= 2 else tier_a
        selected_b = tier_b.sample(n=2) if len(tier_b) >= 2 else tier_b
        selected_c = tier_c.sample(n=2) if len(tier_c) >= 2 else tier_c
        
        # Concatenate the selected customers
        selected_agent_customers = pd.concat([selected_a, selected_b, selected_c])
        
        # Append to the final dataframe
        selected_customers = pd.concat([selected_customers, selected_agent_customers])
    
    return selected_customers

# Select customers
selected_customers_df = select_customers(df)

# Save the selected customers to a new Excel file
output_file_path = 'selected_customers.xlsx'
selected_customers_df.to_excel(output_file_path, index=False)

print(f"Selected customers have been saved to {output_file_path}.")
