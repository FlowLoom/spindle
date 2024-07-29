#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: $0 -d <source_directory> [-s <sprint_id>] [-g <tags>]"
    exit 1
}

# Parse command-line arguments
while getopts "d:s:g:" opt; do
    case $opt in
        d) src_dir=$OPTARG ;;
        s) sprint_id=$OPTARG ;;
        g) tags=$OPTARG ;;
        *) usage ;;
    esac
done

# Check if required arguments are provided
if [ -z "$dest_dir" ]; then
    usage
fi

# Default sprint ID if not provided
if [ -z "$sprint_id" ]; then
    sprint_id=76
fi

# Default tags if not provided
if [ -z "$tags" ]; then
    tags="Josh-Bot"
fi

# Run spindle ticket jira command for each fab_tickets JSON file
for file in "$src_dir"/fab_tickets_*.json; do
    echo "Processing file $file with spindle ticket jira"
    spindle ticket jira create --file="$file" --close --sprint="$sprint_id" --tags="$tags"
done

echo "All files processed."
