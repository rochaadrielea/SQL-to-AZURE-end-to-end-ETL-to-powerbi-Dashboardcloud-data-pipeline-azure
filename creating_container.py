from azure.storage.blob import BlobServiceClient

connection_string = ""
container_name = "manufacturingdata"  # Change this to your desired container name

try:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    if not container_client.exists():
        print(f"Creating container: {container_name}")
        container_client.create_container()
        print("Container created successfully!")
    else:
        print("Container already exists.")

except Exception as e:
    print(f"Error: {e}")
