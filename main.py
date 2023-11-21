import os

from azure.storage.blob import BlobServiceClient

# Azure provided connection-string to authenticate to azure storage account
PLUGIN_CONNECTION_STRING = os.getenv("PLUGIN_CONNECTION_STRING")

# Azure blob container name in which the blobs will be stored
PLUGIN_CONTAINER_NAME = os.getenv("PLUGIN_CONTAINER_NAME")

# Path to your source cache files which are to be uploaded to the blob
PLUGIN_SOURCE = os.getenv("PLUGIN_SOURCE")

# Path under which the files will be uploaded as blob
PLUGIN_BLOB_TARGET = os.getenv("PLUGIN_BLOB_TARGET")

# Bool value (true/false), indicating if the user wants to restore/save cache
PLUGIN_RESTORE = os.getenv("PLUGIN_RESTORE")

# Path to restore and download the files
PLUGIN_RESTORE_TARGET = os.getenv("PLUGIN_RESTORE_TARGET")

# Specified directory that is to be restored from blob
PLUGIN_FETCH_DIR = os.getenv("PLUGIN_FETCH_DIR")

try:
    print("drone-azure-cache")

    # Initialize the BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(PLUGIN_CONNECTION_STRING)

    # Initialize the ContainerClient
    try:
        container_client = blob_service_client.get_container_client(PLUGIN_CONTAINER_NAME)
        print("Container Client: ", container_client)

        if PLUGIN_RESTORE == "true":
            # Restore cache files
            print("Restoring cache...")
            os.makedirs(os.path.dirname(PLUGIN_RESTORE_TARGET), exist_ok=True)
            for blob in container_client.list_blobs():
                # Remove the leading slash from the blob name
                blob_name = blob.name.lstrip('/')
                print("blob_name: ", blob_name)

                # Check if the blob is in the specified folder
                if blob_name.startswith(PLUGIN_FETCH_DIR):
                    relative_path = os.path.relpath(blob_name, PLUGIN_FETCH_DIR)
                    final_path = os.path.join(PLUGIN_RESTORE_TARGET, relative_path)

                    # Ensure the directory structure exists
                    os.makedirs(os.path.dirname(final_path), exist_ok=True)

                    blob_client = container_client.get_blob_client(blob.name)
                    blob_client.download_blob().readinto(open(final_path, 'wb'))
                    print("Restored file: ", blob.name)

        else:
            # Uploading cache files
            print("Uploading cache...")
            for root, dirs, files in os.walk(PLUGIN_SOURCE):
                for file in files:
                    if file.startswith('.'):
                        print(f"Skipping file: {file}")
                        continue

                    # Create the blob name by combining the PLUGIN_TARGET with the relative path
                    relative_path = os.path.relpath(os.path.join(root, file), PLUGIN_SOURCE)
                    blob_name = os.path.join(PLUGIN_BLOB_TARGET, relative_path)

                    print("Uploading file: ", file, "as blob: ", blob_name)

                    blob_client = container_client.get_blob_client(blob_name)
                    with open(os.path.join(root, file), 'rb') as data:
                        blob_client.upload_blob(data, overwrite=True)

    except Exception as ex:
        print('Exception (Initialize the ContainerClient):')
        print(ex)

except Exception as ex:
    print('Exception (Initialize the BlobServiceClient):')
    print(ex)
