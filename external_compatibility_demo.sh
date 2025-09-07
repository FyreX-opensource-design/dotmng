#!/bin/bash
# External Program Compatibility Demo Script
# This script demonstrates the external program compatibility file system

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="${SCRIPT_DIR}/<example-git>"
CONFIG_FILE="${SCRIPT_DIR}/dotfile_config.json"

echo "=========================================="
echo "  External Program Compatibility Demo"
echo "=========================================="
echo

echo "This demo shows how program compatibility settings are now"
echo "stored in an external file for easy updates and maintenance."
echo

echo "1. Listing all compatible programs:"
echo "----------------------------------"
echo "Shows all programs with their compatibility status and categories:"
echo
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --list-compatible-programs
echo

echo "2. Checking program compatibility for a widget:"
echo "----------------------------------------------"
echo "The system now uses the external compatibility file:"
echo
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --check-program-compatibility "<example-widget-1>"
echo

echo "3. Showing the external compatibility file:"
echo "------------------------------------------"
echo "The program compatibility file is located at:"
echo "  ${REPO_PATH}/program_compatibility.json"
echo
echo "File contents (first 20 lines):"
head -20 "${REPO_PATH}/program_compatibility.json"
echo "..."
echo

echo "4. Benefits of external compatibility file:"
echo "------------------------------------------"
echo "✓ Easy to update without modifying main code"
echo "✓ Can be shared across multiple dotfile repositories"
echo "✓ Can be updated from remote URLs"
echo "✓ Includes rich metadata (categories, descriptions)"
echo "✓ Version controlled and maintainable"
echo "✓ Can be customized per repository"
echo

echo "5. Updating compatibility file:"
echo "------------------------------"
echo "You can update the compatibility file from:"
echo "  - Local file: --update-compatibility /path/to/file.json"
echo "  - Remote URL: --update-compatibility https://example.com/compatibility.json"
echo

echo "=========================================="
echo "External Program Compatibility Features:"
echo "✓ External JSON file for easy maintenance"
echo "✓ Rich metadata with categories and descriptions"
echo "✓ Version tracking and update timestamps"
echo "✓ Can be updated from local files or URLs"
echo "✓ Fallback to defaults if file not found"
echo "✓ Easy to share across repositories"
echo "✓ Community-maintainable compatibility database"
echo "=========================================="
