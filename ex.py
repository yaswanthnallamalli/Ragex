import pandas as pd

# Load the CSV file
df = pd.read_csv('data/incident_data.csv', encoding='latin')

# Take the first 5 rows
head_df = df.head()

# Save to Excel
head_df.to_excel('data/incident_data_head.xlsx', index=False)

print("Head of the dataset saved as Excel at: data/incident_data_head.xlsx")
