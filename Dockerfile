# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install azure-storage-blob

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variables
ENV PLUGIN_CONNECTION_STRING ""
ENV PLUGIN_CONTAINER_NAME ""
ENV PLUGIN_SOURCE ""
ENV PLUGIN_BLOB_TARGET ""
ENV PLUGIN_RESTORE ""
ENV PLUGIN_RESTORE_TARGET ""

# Run app.py when the container launches
CMD ["python", "/app/main.py"]
