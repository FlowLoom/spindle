#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: $0 -d <destination_directory> -r <repo_path> [-t <total_end_value>]"
    exit 1
}

# Parse command-line arguments
while getopts "d:r:t:" opt; do
    case $opt in
        d) dest_dir=$OPTARG ;;
        r) repo_path=$OPTARG ;;
        t) total=$OPTARG ;;
        *) usage ;;
    esac
done

# Check if required arguments are provided
if [ -z "$dest_dir" ] || [ -z "$repo_path" ]; then
    usage
fi

# Default total value if not provided
if [ -z "$total" ]; then
    total=250
fi

# Create destination directory if it doesn't exist
mkdir -p "$dest_dir"

# Initial values
start=0
batch_size=5

# Loop until start is greater than total
while [ $start -lt $total ]; do
    # Calculate the end value for the current batch
    end=$((start + batch_size))
    if [ $end -gt $total ]; then
        end=$total
    fi

    echo "Running command with start=$start and end=$end"

    # Generate a timestamp
    timestamp=$(date +"%Y%m%d_%H%M%S")

    # Execute the command with current start and end values, including the timestamp in the output filename
    spindle git --repo="$repo_path" --format=json --output="$dest_dir/tickets_${timestamp}.json" --start=$start --end=$end --full-message | fabric -sp git_tickets_json > "$dest_dir/fab_tickets_${timestamp}.json"

    # Increment start value by batch size
    start=$((start + batch_size))
done

# Record the repository and last commit index processed
echo "Repo: $repo_path, Last Commit Index Processed: $((start - batch_size))" > "$dest_dir/record.txt"

echo "Processing complete. Record saved to $dest_dir/record.txt"
