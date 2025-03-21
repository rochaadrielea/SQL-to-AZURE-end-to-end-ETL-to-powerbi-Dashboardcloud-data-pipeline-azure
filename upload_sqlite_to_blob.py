from azure.storage.blob import BlobServiceClient

# Azure Storage credentials
AZURE_STORAGE_CONNECTION_STRING = ""
CONTAINER_NAME = "manufacturingdata"  # Make sure this matches your created container
BLOB_NAME = "manufacturing_qc.db"  # The name of your database file

# Connect to Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

# Upload SQLite database
with open("manufacturing_qc.db", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print(f"SQLite database '{BLOB_NAME}' uploaded to Azure Blob Storage!")
