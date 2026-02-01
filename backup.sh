#!/bin/bash

# Mindsymphony Backup Script
# Creates timestamped backups of the Mindsymphony skill file

# Get current date and time
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Define backup directory
BACKUP_DIR="./backups"
BACKUP_NAME="mindsymphony_backup_${TIMESTAMP}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# Create backup directory
echo "Creating backup directory: ${BACKUP_PATH}"
mkdir -p "${BACKUP_PATH}"

# Copy the skill file
echo "Copying Mindsymphony skill file..."
cp "mindsymphony _V19.1.skill" "${BACKUP_PATH}/"

# Create a zip archive
echo "Creating zip archive..."
cd "${BACKUP_DIR}"
zip -r "${BACKUP_NAME}.zip" "${BACKUP_NAME}" > /dev/null
cd ..

echo "Backup created successfully!"
echo "Location: ${BACKUP_PATH}"
echo "Archive: ${BACKUP_DIR}/${BACKUP_NAME}.zip"
