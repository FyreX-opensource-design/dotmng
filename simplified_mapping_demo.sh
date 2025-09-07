#!/bin/bash
# Simplified File Mapping Demo Script
# This script demonstrates the simplified file mapping system

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="${SCRIPT_DIR}/<example-git>"
CONFIG_FILE="${SCRIPT_DIR}/dotfile_config.json"

echo "=========================================="
echo "  Simplified File Mapping Demo"
echo "=========================================="
echo

echo "This demo shows how the dotfile manager now automatically"
echo "maps folder names to their .config destinations without"
echo "requiring explicit file mappings in the configuration."
echo

echo "1. Showing widget information with automatic mapping:"
echo "---------------------------------------------------"
echo "Notice how folder names are automatically mapped to .config directories:"
echo
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --info "<example-widget-1>"
echo

echo "2. File mapping examples:"
echo "------------------------"
echo "✓ 'kitty' folder → ~/.config/kitty/"
echo "✓ 'eww' folder → ~/.config/eww/"
echo "✓ 'hyprland' folder → ~/.config/hyprland/"
echo "✓ 'picom' folder → ~/.config/picom/"
echo "✓ 'alacritty' folder → ~/.config/alacritty/"
echo

echo "3. Custom mappings still work:"
echo "-----------------------------"
echo "The 'eww, fabirc, or weld' folder is still mapped to 'eww'"
echo "via the custom_mappings configuration."
echo

echo "4. Benefits of simplified mapping:"
echo "--------------------------------"
echo "✓ No need to maintain file_mappings in config"
echo "✓ Intuitive: folder name = config directory name"
echo "✓ Less configuration to manage"
echo "✓ Automatic support for new programs"
echo "✓ Custom mappings still available when needed"
echo "✓ Cleaner configuration files"
echo

echo "5. Configuration file comparison:"
echo "-------------------------------"
echo "Before (with file_mappings):"
echo "  {"
echo "    \"file_mappings\": {"
echo "      \"kitty\": \"kitty\","
echo "      \"alacritty\": \"alacritty\","
echo "      \"eww\": \"eww\","
echo "      \"hyprland\": \"hyprland\""
echo "    }"
echo "  }"
echo
echo "After (simplified):"
echo "  {"
echo "    \"custom_mappings\": {"
echo "      \"<widget-name>\": {"
echo "        \"special-folder-name\": \"target-name\""
echo "      }"
echo "    }"
echo "  }"
echo

echo "=========================================="
echo "Simplified File Mapping Features:"
echo "✓ Automatic folder-to-config mapping"
echo "✓ No redundant file_mappings needed"
echo "✓ Custom mappings for special cases"
echo "✓ Cleaner, simpler configuration"
echo "✓ Intuitive and self-documenting"
echo "✓ Easy to add new programs"
echo "=========================================="
