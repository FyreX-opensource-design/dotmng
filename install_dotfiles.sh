#!/bin/bash
# Dotfile Manager Installation Script
# This script demonstrates how to use the dotfile manager

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="${SCRIPT_DIR}/<example-git>"

echo "Dotfile Manager - Installation Script"
echo "====================================="
echo

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Make the dotfile manager executable
chmod +x "${SCRIPT_DIR}/dotfile_manager.py"

echo "Available commands:"
echo "==================="
echo

echo "1. List all available widgets:"
echo "   python3 ${SCRIPT_DIR}/dotfile_manager.py ${REPO_PATH} --list"
echo

echo "2. Show information about a specific widget:"
echo "   python3 ${SCRIPT_DIR}/dotfile_manager.py ${REPO_PATH} --info '<example-widget-1>'"
echo

echo "3. Install all widgets (dry run first):"
echo "   python3 ${SCRIPT_DIR}/dotfile_manager.py ${REPO_PATH} --dry-run"
echo "   python3 ${SCRIPT_DIR}/dotfile_manager.py ${REPO_PATH}"
echo

echo "4. Install a specific widget:"
echo "   python3 ${SCRIPT_DIR}/dotfile_manager.py ${REPO_PATH} --widget '<example-widget-1>'"
echo

echo "5. Override environment detection:"
echo "   python3 ${SCRIPT_DIR}/dotfile_manager.py ${REPO_PATH} --environment '{\"window_manager\": \"hyprland\"}'"
echo

echo "6. Install without backing up existing files:"
echo "   python3 ${SCRIPT_DIR}/dotfile_manager.py ${REPO_PATH} --no-backup"
echo

echo "Running example commands..."
echo

# List widgets
echo "Listing available widgets:"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --list
echo

# Show widget info
echo "Showing information about example-widget-1:"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --info "<example-widget-1>"
echo

# Dry run
echo "Performing dry run installation:"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --dry-run
echo

echo "Installation script completed!"
echo "To actually install the dotfiles, run:"
echo "   python3 ${SCRIPT_DIR}/dotfile_manager.py ${REPO_PATH}"

