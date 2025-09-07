# Dotfile Manager

A flexible and intelligent dotfile management system that automatically detects your system environment and installs the appropriate configuration files.

## Features

- **Environment Detection**: Automatically detects your environment and uses folder structure for configuration selection
- **Hierarchical Configuration**: Supports environment-specific configs with fallback to defaults
- **Automatic File Mapping**: Automatically maps folder names to `.config` directories
- **Flexible File Structure**: Handles complex directory structures like `eww, fabirc, or weld`
- **Git Repository Support**: Pull configurations from Git repositories with compatibility checking
- **Repository Management**: Maintain a curated list of compatible dotfile repositories
- **Automatic Metadata Fetching**: Extract descriptions and tags from repository metadata files
- **Tag-based Filtering**: Filter repositories by tags (e.g., hyprland, eww, theme)
- **Backup System**: Automatically backs up existing configuration files
- **Dry Run Mode**: Preview changes before applying them
- **CLI Interface**: Easy-to-use command-line interface

## File Structure

The dotfile manager expects the following structure:

```
<example-git>/                    # Git repository root
├── <widget-name>/               # Widget/theme name
│   ├── default/                 # Fallback configuration
│   │   └── <program>/          # Program-specific configs
│   │       └── config files
│   ├── hyprland/               # Hyprland-specific config
│   │   └── <program>/
│   │       └── config files
│   ├── labwc/                  # LabWC-specific config
│   │   └── <program>/
│   │       └── config files
│   └── <other-environments>/   # Other environment configs
└── <other-widgets>/
```

## Installation

1. Clone or download the dotfile manager
2. Make the script executable:
   ```bash
   chmod +x dotfile_manager.py
   ```

## Usage

### Basic Commands

```bash
# List all available widgets
python3 dotfile_manager.py <repo-path> --list

# Show information about a specific widget
python3 dotfile_manager.py <repo-path> --info "<widget-name>"

# Install all widgets (dry run first)
python3 dotfile_manager.py <repo-path> --dry-run
python3 dotfile_manager.py <repo-path>

# Install a specific widget
python3 dotfile_manager.py <repo-path> --widget "<widget-name>"
```

### Advanced Options

```bash
# Override environment detection
python3 dotfile_manager.py <repo-path> --environment '{"window_manager": "hyprland"}'

# Install without backing up existing files
python3 dotfile_manager.py <repo-path> --no-backup

# Use custom configuration file
python3 dotfile_manager.py <repo-path> --config my_config.json
```

### Git Repository Management

```bash
# List available Git repositories
python3 dotfile_manager.py <repo-path> --list-repos

# Filter repositories by tags
python3 dotfile_manager.py <repo-path> --list-repos --filter-tags "hyprland,theme"

# Add a repository to the compatible list (name and metadata automatically extracted)
python3 dotfile_manager.py <repo-path> --add-repo "https://github.com/user/repo.git"

# Add with manual description (disables metadata fetching)
python3 dotfile_manager.py <repo-path> --add-repo "https://github.com/user/repo.git" "Manual description" --no-fetch-metadata

# Install from a Git repository
python3 dotfile_manager.py <repo-path> --install-from-git "repo-name"

# Install specific widget from Git repository
python3 dotfile_manager.py <repo-path> --install-from-git "repo-name" --git-widget "widget-name"

# Force update repository before installation
python3 dotfile_manager.py <repo-path> --install-from-git "repo-name" --force-update
```

### Quick Start

Run the installation script to see examples:

```bash
./install_dotfiles.sh
```

## Configuration

The dotfile manager uses a JSON configuration file (`dotfile_config.json`) to customize behavior:

```json
{
  "environment_detection": {
    "window_manager": ["hyprland", "labwc", "sway", "i3"],
    "compositor": ["picom", "compton", "xcompmgr"],
    "shell": ["bash", "zsh", "fish"],
    "terminal": ["alacritty", "kitty", "st", "urxvt"]
  },
  "file_mappings": {
    "eww": "eww",
    "hyprland": "hyprland",
    "alacritty": "alacritty"
  },
  "backup_existing": true,
  "create_backup_dir": true,
  "dry_run": false
}
```

## Environment Detection

The manager automatically detects:

- **Window Manager**: Hyprland, LabWC, Sway, i3
- **Compositor**: Picom, Compton, xcompmgr
- **Shell**: Bash, Zsh, Fish
- **Terminal**: Alacritty, Kitty, st, urxvt

## Configuration Selection Logic

1. **Exact Match**: If a configuration directory matches your detected environment exactly
2. **Partial Match**: If a configuration directory contains parts of your environment
3. **Default Fallback**: Uses the `default/` directory if no better match is found

## File Mapping

The manager automatically maps configuration files to their target locations:

- **Automatic Mapping**: Files in `<program>/` directories are copied to `~/.config/<program>/`
- **Intuitive**: Folder name directly corresponds to config directory name
- **Custom Mappings**: Special cases can be handled with custom mappings in the configuration file
- **Complex Names**: Special handling for complex directory names like `eww, fabirc, or weld`

## Backup System

- Existing configuration files are automatically backed up to `~/.config_backup/`
- Backup files are numbered if conflicts occur
- Can be disabled with `--no-backup` flag

## Examples

### Example Widget Structure

```
<example-widget-1>/
├── default/
│   └── eww, fabirc, or weld/
│       └── config.eww
├── hyprland/
│   └── eww, fabirc, or weld/
│       └── config.eww
└── labwc/
    └── eww, fabirc, or weld/
        └── config.eww
```

### Environment-Specific Configurations

- **Hyprland**: Uses Hyprland-specific EWW configuration with workspace indicators
- **LabWC**: Uses LabWC-specific EWW configuration with workspace indicators  
- **Default**: Uses basic EWW configuration without environment-specific features

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure the script has execute permissions
2. **Python Not Found**: Install Python 3 and ensure it's in your PATH
3. **Config Not Found**: Check that your repository path is correct
4. **Backup Failed**: Ensure you have write permissions to your home directory

### Debug Mode

Add `--dry-run` to see what the manager would do without making changes:

```bash
python3 dotfile_manager.py <repo-path> --dry-run
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Feel free to modify and distribute as needed.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Run with `--dry-run` to debug
3. Check the configuration file format
4. Verify your file structure matches the expected format
