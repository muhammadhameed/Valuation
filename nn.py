import pandas as pd
import json

# Read the Excel file into a pandas DataFrame
df = pd.read_excel('fin_stock.xlsx')

# Remove rows with None values in the 'Subsector' column
df = df.dropna(subset=['Subsector'])

# Define a function to parse the types from the JSON object
def parse_types(cell):
    try:
        json_data = json.loads(cell)  # Load cell value as JSON object
        types_list = json_data.get('type', '').split(', ')  # Extract types list
        return types_list
    except (json.JSONDecodeError, AttributeError):
        return []

# Apply the function to each cell in the "Subsector" column
df['Types'] = df['Subsector'].apply(parse_types)

# Function to filter DataFrame based on given types
def filter_by_types(types_list):
    filtered_df = df[df['Types'].apply(lambda x: any(t in x for t in types_list))]
    return filtered_df

# Example usage:
# types_to_filter = ['FineDining']
types_to_filter = ['FineDining', 'CasualDining']
filtered_df = filter_by_types(types_to_filter)
print(df['Country'].unique())
