#!/bin/bash

log_file="$HOME/.config/spindle/install.log"

logging() {
    echo "$(date) : $1"
}

src_dir="./patterns/*"
dest_dir="$HOME/.config/spindle/patterns"

# Create the destination directory if not exists
logging 'Creating destination directory if not exists.'
mkdir -p "$dest_dir"

# Copy and overwrite the files
logging 'Copying and overwriting the files.'
cp -rf $src_dir $dest_dir
logging 'Files copied successfully.'
