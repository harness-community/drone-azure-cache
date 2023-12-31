# drone-azure-cache

Drone plugin to implement Save/Restore Cache functionality using Azure Blob Storage. The purpose is to reduce build times by reusing the cache files.

## What does the "drone-azure-cache" plugin actually do?
The plugin image is based on a minimal base image which will have the necessary tools installed, such as the AzureCLI. When the container runs, it will execute a program that executes the given use-case through the Blob Storage using Azure CLI commands. The cache can either be saved or restored based on a boolean input. The plugin can be integrated in Harness CI using the Pipeline Studio as well. 

## Build and Run using terminal

Clone the repo and use the following commands to run the script directly from the terminal. Make sure to export the respective environment variables.

```bash
pip install azure-storage-blob
python /path/to/repo/main.py
```

## Build using Docker

Build the Docker image with the following commands. Using the following command, the image can be built for different OS and architecture. For example, the below command builds the image for linux/amd64 platform. 

```
docker buildx build -t DOCKER_ORG/drone-azure-cache --platform linux/amd64 .
```
Use the following command to run the container using docker
```bash
# Save cache to Azure Blob storage
docker run --rm \                                                                                                                                                                  
-e PLUGIN_CONNECTION_STRING="your-azure-connection-string" \
-e PLUGIN_CONTAINER_NAME="blob-container-name" \
-e PLUGIN_SOURCE="path/to/source" \
-e PLUGIN_BLOB_TARGET="path/to/target/directory" \
-e PLUGIN_RESTORE="false" \
DOCKER_ORG/drone-azure-cache

# Restore cache from Azure Blob storage
docker run --rm \                                                                                                                                                                  
-e PLUGIN_CONNECTION_STRING="your-azure-connection-string" \
-e PLUGIN_CONTAINER_NAME="blob-container-name" \
-e PLUGIN_RESTORE="true" \
-e PLUGIN_RESTORE_TARGET="path/to/restore/cache" \
-e PLUGIN_FETCH_DIR="directory-to-be-restored" \
DOCKER_ORG/drone-azure-cache
```

## Usage in Harness CI

In Harness CI, the plugin can be implemented in a pipeline as a Plugin step in the Stages using the Pipeline Studio.
![Pipeline Image](images/pipeline.png)

Alternatively, the following YAML can be used to implement the plugin as a step
```yaml
# Save cache to Azure Blob storage
              - step:
                  type: Plugin
                  name: save_cache_azure
                  identifier: save_cache_azure
                  spec:
                    connectorRef: account.harnessImage
                    image: harnesscommunity/drone-azure-cache
                    settings:
                      connection_string: <+secrets.getValue("azureconnectionstring")>
                      container_name: mycontainer
                      source: /path/to/source
                      blob_target: /myblob
                      restore: "false"

# Restore cache from Azure Blob storage
              - step:
                  type: Plugin
                  name: restore_cache_azure
                  identifier: restore_cache_azure
                  spec:
                    connectorRef: account.harnessImage
                    image: harnesscommunity/drone-azure-cache
                    settings:
                      connection_string: <+secrets.getValue("azureconnectionstring")>
                      container_name: mycontainer
                      restore: "false"
                      restore_target: /path/to/restore
                      fetch_dir: /myblob
```
