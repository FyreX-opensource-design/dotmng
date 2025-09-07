#!/bin/bash
# URL-based Repository Addition Demo
# This script demonstrates the new automatic name extraction feature

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="${SCRIPT_DIR}/<example-git>"
CONFIG_FILE="${SCRIPT_DIR}/dotfile_config.json"

echo "=========================================="
echo "  URL-based Repository Addition Demo"
echo "=========================================="
echo

echo "This demo shows how repository names are automatically extracted from URLs:"
echo

echo "1. Adding repository with automatic name extraction:"
echo "---------------------------------------------------"
echo "Command: --add-repo 'https://github.com/example/awesome-theme.git' 'An awesome theme'"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --add-repo "https://github.com/example/awesome-theme.git" "An awesome theme" --filter-tags "theme,awesome"
echo

echo "2. Adding repository with just URL (minimal usage):"
echo "--------------------------------------------------"
echo "Command: --add-repo 'https://github.com/user/minimal-config.git'"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --add-repo "https://github.com/user/minimal-config.git"
echo

echo "3. Adding repository with custom name override:"
echo "----------------------------------------------"
echo "Command: --add-repo 'https://github.com/user/very-long-repository-name.git' 'A custom name' 'my-custom-name'"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --add-repo "https://github.com/user/very-long-repository-name.git" "A custom name" "my-custom-name"
echo

echo "4. Listing all repositories to see the results:"
echo "----------------------------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --list-repos
echo

echo "5. Cleaning up test repositories:"
echo "--------------------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --remove-repo "awesome-theme"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --remove-repo "minimal-config"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --remove-repo "my-custom-name"
echo "Cleanup completed!"
echo

echo "=========================================="
echo "Key benefits of automatic name extraction:"
echo "✓ No need to manually specify repository names"
echo "✓ Reduces errors from typos in names"
echo "✓ Works with GitHub, GitLab, Bitbucket, and other Git hosts"
echo "✓ Still allows custom name override when needed"
echo "✓ Handles .git suffix automatically"
echo "=========================================="
