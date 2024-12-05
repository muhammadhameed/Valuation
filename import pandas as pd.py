import pandas as pd
import ast

# Read the Excel file into a pandas DataFrame
df = pd.read_excel('your_excel_file.xlsx')

# Define a function to parse the types from the string
def parse_types(cell):
    types_str = cell.strip('{}')  # Remove curly braces from the string
    types_list = ast.literal_eval(types_str)  # Convert string to list
    return types_list

# Apply the function to each cell in the "Subsector" column
df['Types'] = df['Subsector'].apply(parse_types)

# Create a set to store unique types
unique_types = set()

# Iterate through the "Types" column to collect unique types
for types_list in df['Types']:
    unique_types.update(types_list)

# Convert the set of unique types into a sorted list
unique_types_list = sorted(list(unique_types))

# Print the list of unique types
print(unique_types_list)
