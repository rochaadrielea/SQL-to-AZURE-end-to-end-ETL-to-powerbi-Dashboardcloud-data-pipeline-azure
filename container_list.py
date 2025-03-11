from azure.storage.blob import BlobServiceClient

# Replace with your storage account connection string
connection_string = ""
try:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    containers = blob_service_client.list_containers()
    
    print("Available containers:")
    for container in containers:
        print(container["name"])

except Exception as e:
    print(f"Error: {e}")
