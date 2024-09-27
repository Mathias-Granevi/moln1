import json
import pyodbc
from azure.storage.queue import QueueServiceClient
import os

# Azure Storage Queue configuration
queue_name = "myqueue"
connection_string = os.environ.get("CONNECTION_STRING")

# Azure SQL Database configuration
sql_server = 'de23testing2.database.windows.net'
database = 'pipelineDB'
username = 'mathias'
password = os.environ.get("DATABASE_PASSWORD")
table_name = 'CrimeStatistics'

# Create a QueueServiceClient
queue_service_client = QueueServiceClient.from_connection_string(connection_string)
queue_client = queue_service_client.get_queue_client(queue_name)

# Connect to Azure SQL Database
conn_str = f"Driver={{ODBC Driver 18 for SQL Server}};Server={sql_server};Database={database};UID={username};PWD={password}"
connection = pyodbc.connect(conn_str)
cursor = connection.cursor()

# Define a maximum number of iterations to prevent infinite loop
max_iterations = 100
iteration_count = 0

# Fetch messages from the queue and insert into the SQL database
while iteration_count < max_iterations:
    messages = queue_client.receive_messages(messages_per_page=32)

    for row in messages:
        # Parse the JSON message
        data = json.loads(row.content)

        # Insert data into the SQL database
        cursor.execute("""
        INSERT INTO CrimeStatistics (Year, Crimes_Total, Crimes_Penal_Code, Crimes_Person,
        Murder, Assault, Sexual_Offenses, Rape, Stealing_General, Burglary,
        House_Theft, Vehicle_Theft, Out_Of_Vehicle_Theft, Shop_Theft, Robbery,
        Fraud, Criminal_Damage, Other_Penal_Crimes, Narcotics, Drunk_Driving, Population)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            int(data['Year']),
            int(data['crimes_total']),
            int(data['crimes_penal_code']),
            int(data['crimes_person']),
            int(data['murder']),
            int(data['assault']),
            int(data['sexual_offenses']),
            int(data['rape']),
            int(data['stealing_general']),
            int(data['burglary']),
            int(data['house_theft']),
            int(data['vehicle_theft']),
            int(data['out_of_vehicle_theft']),
            int(data['shop_theft']),
            int(data['robbery']),
            int(data['fraud']),
            int(data['criminal_damage']),
            int(data['other_penal_crimes']),
            int(data['narcotics']),
            int(data['drunk_driving']),
            int(data['population'])
        ))

        # Delete the message from the queue after processing
        queue_client.delete_message(row)

    # Commit the transaction to the database
    connection.commit()

    # Increment the iteration count
    iteration_count += 1

# Close the database connection
cursor.close()
connection.close()

print("Messages processed and inserted into the database successfully!")
