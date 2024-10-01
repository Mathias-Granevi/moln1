import json
import pandas as pd
from azure.storage.queue import QueueServiceClient
import os

# Load JSON data
with open('cleaned_reported.json', 'r') as f:
    data = json.load(f)

# Convert JSON data to DataFrame
df = pd.DataFrame(data)

# Azure Storage Queue configuration
queue_name = "myqueue"
connection_string = os.environ.get("CONNECTION_STRING")

# Create a QueueServiceClient
queue_service_client = QueueServiceClient.from_connection_string(connection_string)
queue_client = queue_service_client.get_queue_client(queue_name)

# Send each row of the DataFrame as a message
for _, row in df.iterrows():
    message = row.to_json()
    print(message)  # Print the JSON message for debugging
    queue_client.send_message(message)


print("Data sent to queue successfully!")