#!/bin/bash

# Ask for the necessary details
echo "Enter the path to your GCP service account JSON file:"
read GCP_JSON_PATH
echo "Enter the GCP project ID (or leave blank to list available projects):"
read PROJECT_ID
echo "Enter the network name for the container:"
read NETWORK_NAME
echo "Enter the container name:"
read CONTAINER_NAME
echo "Enter the port for Steampipe (e.g., 9002):"
read STEAMPIPE_PORT
echo "Enter the port for Powerpipe (e.g., 9102):"
read POWERPIPE_PORT

# Check if the Docker network exists, create it if not
docker network inspect $NETWORK_NAME > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Network $NETWORK_NAME does not exist. Creating it..."
  docker network create $NETWORK_NAME
else
  echo "Network $NETWORK_NAME already exists."
fi

# Build the Docker image (if not already built)
docker build -t gcp-powerpipe-steampipe .

# Remove any existing container with the same name
docker rm -f $CONTAINER_NAME > /dev/null 2>&1

# Create and start the Docker container
docker run -d --name $CONTAINER_NAME \
  --network $NETWORK_NAME \
  -p $STEAMPIPE_PORT:$STEAMPIPE_PORT \
  -p $POWERPIPE_PORT:$POWERPIPE_PORT \
  -v $GCP_JSON_PATH:/home/powerpipe/.gcp-service-account.json \
  gcp-powerpipe-steampipe

# Wait for the container to start
echo "Waiting for the container $CONTAINER_NAME to start..."
sleep 5  # Wait for 5 seconds to allow the container to initialize

# Enter the container automatically
docker exec -it $CONTAINER_NAME /bin/bash
