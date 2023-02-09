import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('hosteldatabase.db')

# Read data from the Excel sheet
data = pd.read_excel('data.xlsx')

# Insert the data into the SQLite database
data.to_sql('students', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
