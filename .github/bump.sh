#!/bin/bash

# Get current version
PREV_VER="$(<version.txt)"
echo "Previous version:"
echo $PREV_VER

# Split the version into an array of 
# Major, minor, patch
# read -a splits the arguments into an array
read -r -a versions <<< $(echo $PREV_VER | tr '.' ' ')

# Increment patch version
patch_ver=$(( ${versions[2]} + 1))

# Get the new version
NEW_VER="${versions[0]}.${versions[1]}.${patch_ver}"
echo "New version:"
echo $NEW_VER
echo $NEW_VER > version.txt


