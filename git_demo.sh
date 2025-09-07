#!/bin/bash
# Git Repository Management Demo Script
# This script demonstrates the Git repository features of the dotfile manager

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="${SCRIPT_DIR}/<example-git>"
CONFIG_FILE="${SCRIPT_DIR}/dotfile_config.json"

echo "=========================================="
echo "  Dotfile Manager - Git Repository Demo"
echo "=========================================="
echo

echo "1. Listing available Git repositories:"
echo "-------------------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --list-repos
echo

echo "2. Filtering repositories by tags (hyprland):"
echo "--------------------------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --list-repos --filter-tags "hyprland"
echo

echo "3. Adding a new repository:"
echo "-------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --add-repo "test-repo" "https://github.com/example/test-repo.git" "A test repository" --filter-tags "test,example"
echo

echo "4. Listing repositories after adding:"
echo "------------------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --list-repos
echo

echo "5. Checking compatibility of a local directory:"
echo "----------------------------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --check-compatibility "${REPO_PATH}"
echo

echo "6. Removing the test repository:"
echo "-------------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --remove-repo "test-repo"
echo

echo "7. Listing repositories after removal:"
echo "-------------------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --list-repos
echo

echo "=========================================="
echo "Git Repository Demo completed!"
echo
echo "To install from a Git repository, you would run:"
echo "  python3 ${SCRIPT_DIR}/dotfile_manager.py ${REPO_PATH} --config ${CONFIG_FILE} --install-from-git <repo-name>"
echo
echo "To install a specific widget from a Git repository:"
echo "  python3 ${SCRIPT_DIR}/dotfile_manager.py ${REPO_PATH} --config ${CONFIG_FILE} --install-from-git <repo-name> --git-widget <widget-name>"
echo
echo "To force update a Git repository:"
echo "  python3 ${SCRIPT_DIR}/dotfile_manager.py ${REPO_PATH} --config ${CONFIG_FILE} --install-from-git <repo-name> --force-update"
echo "=========================================="

