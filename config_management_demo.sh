#!/bin/bash
# Configuration Management Demo Script
# This script demonstrates the new configuration management features

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="${SCRIPT_DIR}/<example-git>"
CONFIG_FILE="${SCRIPT_DIR}/dotfile_config.json"

echo "=========================================="
echo "  Configuration Management Demo"
echo "=========================================="
echo

echo "This demo shows the new configuration management features:"
echo "1. Pull existing configurations from ~/.config to repository structure"
echo "2. Use ~/.config as fallback when installing widgets"
echo

echo "1. Pull from ~/.config to Repository Structure:"
echo "---------------------------------------------"
echo "This feature allows you to backup your existing configurations"
echo "to the repository structure for version control and sharing."
echo "It's now SAFE and SELECTIVE - only pulls relevant dotfile programs!"
echo

echo "Example: Pull all relevant configs automatically:"
echo "python3 dotfile_manager.py <repo-path> --pull-from-config my-configs"
echo

echo "Example: Pull specific programs only:"
echo "python3 dotfile_manager.py <repo-path> --pull-from-config my-configs --specific-programs alacritty kitty eww"
echo

echo "Example: Pull to custom output directory:"
echo "python3 dotfile_manager.py <repo-path> --pull-from-config my-configs --output-dir /path/to/custom/dir"
echo

echo "2. Config Fallback Feature:"
echo "-------------------------"
echo "When a widget doesn't exist in the repository, you can use"
echo "~/.config as a fallback source for installation."
echo

echo "Example: Install 'nonexistent-widget' using ~/.config as fallback:"
echo "python3 dotfile_manager.py <repo-path> --widget nonexistent-widget --use-config-fallback"
echo

echo "3. Safety Features:"
echo "-----------------"
echo "✓ Only pulls relevant dotfile programs (no system directories)"
echo "✓ Excludes browser data, caches, and system configs"
echo "✓ Asks for confirmation when pulling many configs"
echo "✓ Comprehensive file filtering (locks, sockets, databases, etc.)"
echo "✓ Can specify exact programs to pull"
echo "✓ Can specify custom output directory"
echo

echo "4. Real-World Use Cases:"
echo "----------------------"
echo "✓ Backup existing configurations to repository"
echo "✓ Share configurations with others via repository"
echo "✓ Use existing configs when repository doesn't have them"
echo "✓ Migrate from manual config management to dotfile manager"
echo "✓ Sync local changes back to repository structure"
echo "✓ Export configs to custom directories for sharing"
echo "✓ Create temporary config collections"
echo

echo "5. Configuration File Locations:"
echo "------------------------------"
echo "The system now looks for configuration files in this priority order:"
echo "1. Script directory (where dotfile_manager.py is located)"
echo "2. Repository path (fallback)"
echo "3. ~/.config directory (final fallback)"
echo

echo "Configuration files that support fallback:"
echo "  - dotfile_config.json"
echo "  - program_compatibility.json"
echo "  - compatible_repos.txt"
echo "  - auto_config_rules.json (NEW!)"
echo

echo "Files moved to correct locations:"
echo "  - compatible_repos.txt → /home/nathan/dotmng/"
echo "  - program_compatibility.json → /home/nathan/dotmng/"
echo "  - auto_config_rules.json → /home/nathan/dotmng/ (NEW!)"
echo

echo "6. Benefits of New Features:"
echo "--------------------------"
echo "✓ Bidirectional configuration management"
echo "✓ Easy backup and restore of configurations"
echo "✓ Fallback support for missing repository configs"
echo "✓ Better organization of configuration files"
echo "✓ Support for existing user configurations"
echo "✓ Configuration file fallback from ~/.config"
echo "✓ Flexible configuration file locations"
echo "✓ External auto config rules (customizable filtering)"
echo

echo "7. Example Workflow:"
echo "------------------"
echo "1. Pull existing configs:"
echo "   python3 dotfile_manager.py <repo-path> --pull-from-config my-setup"
echo
echo "2. Install with fallback:"
echo "   python3 dotfile_manager.py <repo-path> --widget my-setup --use-config-fallback"
echo
echo "3. Regular installation:"
echo "   python3 dotfile_manager.py <repo-path> --widget my-setup"
echo
echo "4. Update auto config rules:"
echo "   python3 dotfile_manager.py <repo-path> --update-auto-config-rules <url-or-path>"
echo
echo "5. Pull to custom directory:"
echo "   python3 dotfile_manager.py <repo-path> --pull-from-config my-configs --output-dir /custom/path"
echo

echo "8. Error Handling:"
echo "----------------"
echo "The system handles various edge cases:"
echo "✓ Skips problematic files (locks, sockets, etc.)"
echo "✓ Provides warnings for failed copies"
echo "✓ Continues processing other files"
echo "✓ Graceful fallback when configs don't exist"
echo

echo "=========================================="
echo "Configuration Management Features:"
echo "✓ SAFE pull from ~/.config (selective filtering)"
echo "✓ Use ~/.config as installation fallback"
echo "✓ Configuration file fallback from ~/.config"
echo "✓ Proper file location management"
echo "✓ Error handling and warnings"
echo "✓ Bidirectional configuration sync"
echo "✓ Support for existing user setups"
echo "✓ Flexible configuration file discovery"
echo "✓ User confirmation for large operations"
echo "✓ Comprehensive file filtering"
echo "✓ External auto config rules (customizable)"
echo "✓ Custom output directory support"
echo "=========================================="
