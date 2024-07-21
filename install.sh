#!/bin/bash

src_dir="./patterns/*"
dest_dir="$HOME/.config/fabric/patterns"

# Create the destination directory if not exists
mkdir -p "$dest_dir"

# Copy the files
cp -r $src_dir $dest_dir