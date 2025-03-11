from azure.storage.blob import BlobServiceClient

# Replace with your storage account connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=mdd0303;AccountKey=pQBeyj+E+r633lfi1m957uXfP/9nZDdM/TL3MVKI7Nl5gP1RfYDK/YZCNAFPaRA/NiYwmd4dqgEC+AStOpIHzA==;EndpointSuffix=core.windows.net"

try:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    containers = blob_service_client.list_containers()
    
    print("Available containers:")
    for container in containers:
        print(container["name"])

except Exception as e:
    print(f"Error: {e}")
