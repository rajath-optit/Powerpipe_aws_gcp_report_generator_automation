#!/bin/bash
 
# Parameters

AWS_ACCESS_KEY_ID="$1"

AWS_SECRET_ACCESS_KEY="$2"

AWS_REGION="${3:-us-east-1}"  # Default region is 'us-east-1' if not provided

STEAMPIPE_PORT=9194

POWERPIPE_PORT=9040

IMAGE_NAME="${4:-pp-sp-img}"

DOCKER_NETWORK="${5:-aws_default_network}"

CONTAINER_NAME_BASE="${6:-default_container}"
 
# Debug: Print the provided AWS credentials (not recommended for production use)

echo "AWS Region: $AWS_REGION"

echo "Steampipe Port: $STEAMPIPE_PORT"

echo "Powerpipe Port: $POWERPIPE_PORT"

echo "Docker Network: $DOCKER_NETWORK"

echo "Image Name: $IMAGE_NAME"

echo "Container Name Base: $CONTAINER_NAME_BASE"
 
# Function: Check AWS Credentials

check_aws_credentials() {

    echo "Checking AWS Credentials..."

    AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \

    AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \

    AWS_REGION="$AWS_REGION" \

    aws sts get-caller-identity >/dev/null 2>&1
 
    if [ $? -ne 0 ]; then

        echo "Invalid AWS Credentials or region: $AWS_REGION"

        exit 1

    fi
 
    echo "AWS Credentials are valid."

}
 
# Function: Check Port Availability

check_port_availability() {

    echo "Checking Port Availability..."

    is_port_available() {

        local port=$1

        netstat -tuln | grep -q ":$port " >/dev/null 2>&1

        return $?

    }
 
    is_port_available "$STEAMPIPE_PORT"

    if [ $? -eq 0 ]; then

        echo "Port $STEAMPIPE_PORT is already in use."

        exit 1

    fi
 
    is_port_available "$POWERPIPE_PORT"

    if [ $? -eq 0 ]; then

        echo "Port $POWERPIPE_PORT is already in use."

        exit 1

    fi
 
    echo "Both Steampipe Port ($STEAMPIPE_PORT) and Powerpipe Port ($POWERPIPE_PORT) are available."

}
 
# Function: Create Docker Network

create_docker_network() {

    echo "Checking Docker Network..."

    network_exists=$(sudo docker network ls --filter name="$DOCKER_NETWORK" --format '{{.Name}}')

    if [ -z "$network_exists" ]; then

        sudo docker network create "$DOCKER_NETWORK"

        echo "Created Docker network: $DOCKER_NETWORK"

    else

        echo "Docker network already exists: $DOCKER_NETWORK"

    fi

}
 
# Function: Run Docker Container

run_docker_container() {

    echo "Running Docker Container..."

    for i in 1 2 3; do

        candidate_name="${CONTAINER_NAME_BASE}_$i"

        container_exists=$(sudo docker ps -a --filter name="$candidate_name" --format '{{.Names}}')
 
        if [ -z "$container_exists" ]; then

            container_name="$candidate_name"

            break

        fi

    done
 
    if [ -z "$container_name" ]; then

        echo "All containers (${CONTAINER_NAME_BASE}_1, ${CONTAINER_NAME_BASE}_2, ${CONTAINER_NAME_BASE}_3) are already in use."

        exit 1

    fi
 
    echo "Selected container name: $container_name"
 
    sudo docker run -d --name "$container_name" \

        --network "$DOCKER_NETWORK" \

        -p "$STEAMPIPE_PORT":"$STEAMPIPE_PORT" \

        -p "$POWERPIPE_PORT":"$POWERPIPE_PORT" \

        -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \

        -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \

        -e AWS_REGION="$AWS_REGION" \

        "$IMAGE_NAME"

}
 
# Function: Initialize and Install Modules

initialize_and_install_modules() {

    echo "Initializing and Installing Modules..."

    sudo docker exec -it "$container_name" /bin/bash -c '

        mkdir -p /home/powerpipe/mod && cd /home/powerpipe/mod &&

        powerpipe mod init &&

        powerpipe mod install github.com/turbot/steampipe-mod-aws-compliance &&

        steampipe query "select * from aws_s3_bucket;"

    '

}
 
# Function: Start Services

start_services() {

    echo "Starting Steampipe and Powerpipe Services..."

    sudo docker exec -d "$container_name" /bin/bash -c '

        nohup steampipe service start --port '"$STEAMPIPE_PORT"' > /home/powerpipe/steampipe.log 2>&1 &

        nohup powerpipe server --port '"$POWERPIPE_PORT"' > /home/powerpipe/powerpipe.log 2>&1 &

    '

}
 
# Main Script Execution

check_aws_credentials

check_port_availability

create_docker_network

run_docker_container

initialize_and_install_modules

start_services

 
# ./your_script_name.sh <AWS_ACCESS_KEY_ID> <AWS_SECRET_ACCESS_KEY> [AWS_REGION] [IMAGE_NAME] [DOCKER_NETWORK] [CONTAINER_NAME_BASE]

 
# Example :./setup_docker.sh AKIAEXAMPLE wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY ap-south-1 pp-sp-img aws_default_network my_container

 
