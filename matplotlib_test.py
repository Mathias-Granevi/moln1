import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define connection parameters
sql_server = os.environ.get("SQLSERVER")
database = 'pipelineDB'
username = 'mathias'
password = os.environ.get("DATABASE_PASSWORD")

# Create the connection string
connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={sql_server};Database={database};UID={username};PWD={password}"

# Initialize the connection variable
conn = None

# Establish the connection
try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")
except Exception as e:
    print("Error establishing connection:", e)

# Fetch data from the CrimeStatistics table only if connection is successful
if conn is not None:
    query = "SELECT Year, Crimes_Total FROM CrimeStatistics"
    
    # Use pandas to read the SQL query into a DataFrame
    try:
        df = pd.read_sql(query, conn)
        print("Data fetched successfully!")
        print(df.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print("Error fetching data:", e)
    finally:
        conn.close()  # Close the connection
else:
    print("Connection was not established. Cannot fetch data.")

# If the DataFrame was created, proceed with visualization
if 'df' in locals():  # Check if df was defined
    # Visualize the data using Matplotlib

    # Bar Chart of Total Crimes Over the Years
    plt.figure(figsize=(12, 6))
    plt.bar(df['Year'], df['Crimes_Total'], color=plt.cm.Blues(df['Crimes_Total'] / df['Crimes_Total'].max()))
    plt.title('Total Crimes Over the Years')
    plt.xlabel('Year')
    plt.ylabel('Total Crimes per 100.000 inhabitants')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
    
