#!/bin/bash
# Metadata Fetching Demo Script
# This script demonstrates automatic metadata fetching from repository files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="${SCRIPT_DIR}/<example-git>"
CONFIG_FILE="${SCRIPT_DIR}/dotfile_config.json"

echo "=========================================="
echo "  Metadata Fetching Demo"
echo "=========================================="
echo

echo "This demo shows how the dotfile manager can automatically fetch"
echo "descriptions and tags from metadata files in repositories."
echo

echo "1. Adding repository with automatic metadata fetching:"
echo "----------------------------------------------------"
echo "Command: --add-repo 'file://${REPO_PATH}'"
echo "This will automatically read dotfile-info.json and extract metadata"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --add-repo "file://${REPO_PATH}"
echo

echo "2. Listing repositories to see the fetched metadata:"
echo "--------------------------------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --list-repos
echo

echo "3. Adding repository without metadata fetching:"
echo "---------------------------------------------"
echo "Command: --add-repo 'file://${REPO_PATH}' 'Manual description' --no-fetch-metadata"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --add-repo "file://${REPO_PATH}" "Manual description" "manual-repo" --no-fetch-metadata
echo

echo "4. Listing repositories to compare:"
echo "----------------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --list-repos
echo

echo "5. Cleaning up test repositories:"
echo "--------------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --remove-repo "example-git"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --remove-repo "manual-repo"
echo "Cleanup completed!"
echo

echo "=========================================="
echo "Metadata file formats supported:"
echo "✓ dotfile-info.json (JSON format)"
echo "✓ dotfile-info.yaml (YAML format)"
echo "✓ dotfile-info.yml (YAML format)"
echo "✓ .dotfile-info.json (Hidden JSON file)"
echo "✓ README.md (Basic extraction from markdown)"
echo
echo "Metadata fields supported:"
echo "✓ description - Repository description"
echo "✓ tags - List of tags for categorization"
echo "✓ author - Repository author"
echo "✓ version - Version information"
echo "✓ compatibility - Supported environments"
echo "✓ programs - Supported programs"
echo "✓ license - License information"
echo "✓ homepage - Project homepage"
echo "✓ documentation - Documentation file"
echo "=========================================="
