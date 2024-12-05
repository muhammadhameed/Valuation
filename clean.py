import pandas as pd

# Load the Excel file into a Pandas DataFrame
file_path = 'stock_info.xlsx'  # Replace with the actual file path

df = pd.read_excel(file_path)

# Drop rows with NA values
df = df.dropna()

# Drop rows with duplicate values in the 'Symbol' column
df = df.drop_duplicates(subset='Symbol', keep='first')

# Reset the index after dropping rows
df = df.reset_index(drop=True)

# Save the cleaned DataFrame back to the same Excel file
df.to_excel(file_path, index=False)