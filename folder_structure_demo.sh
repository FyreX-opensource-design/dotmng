#!/bin/bash
# Folder Structure Environment Detection Demo
# This script demonstrates how the folder structure automatically handles environment detection

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="${SCRIPT_DIR}/<example-git>"
CONFIG_FILE="${SCRIPT_DIR}/dotfile_config.json"

echo "=========================================="
echo "  Folder Structure Environment Detection"
echo "=========================================="
echo

echo "This demo shows how the folder structure automatically handles"
echo "environment detection without needing hardcoded configuration."
echo

echo "1. Current Environment Detection:"
echo "--------------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --check-program-compatibility "<example-widget-1>" 2>&1 | grep "Detected environment" || echo "No environment detection output found"
echo

echo "2. Available Configuration Folders:"
echo "----------------------------------"
echo "The system automatically finds these configuration folders:"
echo
find "${REPO_PATH}/<example-widget-1>" -maxdepth 1 -type d -name "*" | grep -v "^${REPO_PATH}/<example-widget-1>$" | sort | while read -r folder; do
    folder_name=$(basename "$folder")
    echo "  - $folder_name"
done
echo

echo "3. Environment Detection Logic:"
echo "------------------------------"
echo "1. Detect current environment (window manager, compositor, etc.)"
echo "2. Look for matching folder in widget directory"
echo "3. If found, use that folder's configuration"
echo "4. If not found, fall back to 'default' folder"
echo "5. No hardcoded environment lists needed!"
echo

echo "4. Example Detection Flow:"
echo "-------------------------"
echo "Current environment: labwc + wayland"
echo "Look for: <example-widget-1>/labwc/"
echo "Found: ✓ Uses labwc configuration"
echo
echo "If environment was: hyprland + wayland"
echo "Look for: <example-widget-1>/hyprland/"
echo "Found: ✓ Uses hyprland configuration"
echo
echo "If environment was: unknown + wayland"
echo "Look for: <example-widget-1>/unknown/"
echo "Not found: ✗ Falls back to default configuration"
echo

echo "5. Benefits of Folder Structure Detection:"
echo "----------------------------------------"
echo "✓ No hardcoded environment lists to maintain"
echo "✓ Automatically supports new environments"
echo "✓ Intuitive: folder name = environment name"
echo "✓ Easy to add new environment support"
echo "✓ Self-documenting structure"
echo "✓ No configuration file updates needed"
echo

echo "6. Adding New Environment Support:"
echo "--------------------------------"
echo "To add support for a new environment (e.g., 'awesome'):"
echo "1. Create folder: <example-widget-1>/awesome/"
echo "2. Add configuration files to that folder"
echo "3. Done! No config file changes needed"
echo

echo "7. Configuration File Simplification:"
echo "-----------------------------------"
echo "Before (with hardcoded environment_detection):"
echo "  {"
echo "    \"environment_detection\": {"
echo "      \"window_manager\": [\"hyprland\", \"labwc\", \"sway\", \"i3\"]"
echo "    }"
echo "  }"
echo
echo "After (folder structure handles it):"
echo "  {"
echo "    \"custom_mappings\": {"
echo "      \"<widget-name>\": {"
echo "        \"special-folder\": \"target-name\""
echo "      }"
echo "    }"
echo "  }"
echo

echo "8. Real-World Example:"
echo "--------------------"
echo "Widget: <example-widget-1>"
echo "Available configurations:"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --info "<example-widget-1>" | grep -A 20 "Available configurations:"
echo

echo "=========================================="
echo "Folder Structure Environment Detection:"
echo "✓ Automatic environment detection"
echo "✓ No hardcoded environment lists"
echo "✓ Intuitive folder-based structure"
echo "✓ Easy to extend and maintain"
echo "✓ Self-documenting configuration"
echo "✓ Fallback to default folder"
echo "=========================================="
