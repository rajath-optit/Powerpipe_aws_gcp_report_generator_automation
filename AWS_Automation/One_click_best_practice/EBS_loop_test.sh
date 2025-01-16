#!/bin/bash

# Log functions for structured output
log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1" | tee -a changes.log
}

error() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] $1" | tee -a changes.log >&2
}

# Ensure log file starts with a timestamp for the run
log_run() {
  echo -e "\n========== Run on $(date '+%Y-%m-%d %H:%M:%S') ==========" >> changes.log
}

# Validate CSV file existence
validate_csv_file() {
  if [[ ! -f $1 ]]; then
    error "CSV file not found: $1. Please provide a valid file."
    exit 1
  fi
  log "CSV file found: $1"
}

# Validate CSV format
validate_csv_format() {
  local required_columns=("resource" "status")
  local header=$(head -1 "$1")
  for col in "${required_columns[@]}"; do
    if ! grep -q "$col" <<<"$header"; then
      error "CSV file does not have the required column: $col"
      exit 1
    fi
  done
  log "CSV file format validated."
}

# Retrieve all available EBS volume IDs in the current region
get_available_volume_ids() {
  aws ec2 describe-volumes --query "Volumes[*].VolumeId" --output text 2>/dev/null
}

# Ensure DeleteOnTermination is enabled for a volume
ensure_delete_on_termination() {
  local volume_id=$1
  log "Checking DeleteOnTermination for volume $volume_id"
  local instance_id=$(aws ec2 describe-volumes --volume-ids "$volume_id" --query "Volumes[0].Attachments[0].InstanceId" --output text 2>/dev/null)
  local device_name=$(aws ec2 describe-volumes --volume-ids "$volume_id" --query "Volumes[0].Attachments[0].Device" --output text 2>/dev/null)
  
  if [[ -z "$instance_id" || -z "$device_name" ]]; then
    log "Volume $volume_id is not attached to an instance or information is unavailable."
    return
  fi
  
  local current_value=$(aws ec2 describe-instance-attribute --instance-id "$instance_id" --attribute blockDeviceMapping \
  --query "BlockDeviceMappings[?DeviceName=='$device_name'].Ebs.DeleteOnTermination" --output text 2>/dev/null)
  
  if [[ "$current_value" != "True" ]]; then
    log "Enabling DeleteOnTermination for volume $volume_id on instance $instance_id"
    aws ec2 modify-instance-attribute --instance-id "$instance_id" --block-device-mappings \
    "[{\"DeviceName\": \"$device_name\", \"Ebs\": {\"DeleteOnTermination\": true}}]" || error "Failed to set DeleteOnTermination for volume $volume_id"
  else
    log "DeleteOnTermination is already enabled for volume $volume_id"
  fi
}

# Ensure encryption is enabled for a volume
ensure_encryption_enabled() {
  local volume_id=$1
  log "Checking encryption for volume $volume_id"
  local encryption_status=$(aws ec2 describe-volumes --volume-ids "$volume_id" --query "Volumes[0].Encrypted" --output text 2>/dev/null)
  
  if [[ "$encryption_status" != "True" ]]; then
    log "Encrypting volume $volume_id"
    aws ec2 encrypt-volume --volume-id "$volume_id" --kms-key-id alias/aws/ebs || error "Failed to encrypt volume $volume_id"
  else
    log "Volume $volume_id is already encrypted"
  fi
}

# Process resources from CSV
process_csv() {
  local csv_file=$1
  local available_volumes=($(get_available_volume_ids))
  
  while IFS=',' read -r resource status; do
    # Skip header row
    [[ $resource == "resource" && $status == "status" ]] && continue
    
    # Skip resources not in alarm state
    if [[ "$status" != "alarm" ]]; then
      log "Skipping resource $resource with status $status (not 'alarm')."
      continue
    fi
    
    # Process only resources available in the current region
    if [[ " ${available_volumes[*]} " == *"${resource##*/}"* ]]; then
      log "Processing EC2 volume: $resource"
      ensure_delete_on_termination "${resource##*/}"
      ensure_encryption_enabled "${resource##*/}"
    else
      log "Skipping resource $resource as it is not available in the current region."
    fi
  done < <(tail -n +2 "$csv_file") # Skip header row
}

# Main function
main() {
  local csv_file=$1
  
  if [[ -z "$csv_file" ]]; then
    error "No CSV file provided. Usage: ./script.sh <csv_file>"
    exit 1
  fi
  
  log_run
  validate_csv_file "$csv_file"
  validate_csv_format "$csv_file"
  process_csv "$csv_file"
}

# Run the script
main "$@"
