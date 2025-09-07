# Git Repository Management Guide

The dotfile manager now supports pulling configurations from Git repositories and managing a curated list of compatible repositories.

## Features

- **Repository List Management**: Maintain a list of compatible dotfile repositories
- **Automatic Cloning**: Clone repositories locally for installation
- **Compatibility Checking**: Verify repositories follow the expected structure
- **Tag-based Filtering**: Filter repositories by tags (e.g., hyprland, eww, theme)
- **Update Management**: Update existing repositories with new changes
- **Selective Installation**: Install specific widgets or all widgets from a repository

## Repository List Format

The `compatible_repos.txt` file uses a simple pipe-separated format:

```
name|url|description|tags (comma-separated)
```

### Example:
```
catppuccin-hyprland|https://github.com/catppuccin/hyprland.git|Catppuccin theme for Hyprland|hyprland,theme,catppuccin
awesome-eww|https://github.com/awesome-eww/awesome-eww.git|Awesome EWW widgets collection|eww,widgets,awesome
```

## Commands

### Repository Management

```bash
# List all available repositories
python3 dotfile_manager.py <repo-path> --list-repos

# Filter repositories by tags
python3 dotfile_manager.py <repo-path> --list-repos --filter-tags "hyprland,theme"

# Add a new repository (name automatically extracted from URL)
python3 dotfile_manager.py <repo-path> --add-repo "https://github.com/user/repo.git" "Description" --filter-tags "tag1,tag2"

# Add with custom name
python3 dotfile_manager.py <repo-path> --add-repo "https://github.com/user/repo.git" "Description" "custom-name"

# Remove a repository
python3 dotfile_manager.py <repo-path> --remove-repo "repo-name"

# Check compatibility of a local directory
python3 dotfile_manager.py <repo-path> --check-compatibility "/path/to/repo"
```

### Installation from Git Repositories

```bash
# Install all widgets from a Git repository
python3 dotfile_manager.py <repo-path> --install-from-git "repo-name"

# Install a specific widget from a Git repository
python3 dotfile_manager.py <repo-path> --install-from-git "repo-name" --git-widget "widget-name"

# Force update a repository before installation
python3 dotfile_manager.py <repo-path> --install-from-git "repo-name" --force-update

# Install with environment override
python3 dotfile_manager.py <repo-path> --install-from-git "repo-name" --environment '{"window_manager": "hyprland"}'
```

## Repository Structure Requirements

For a repository to be compatible, it must follow this structure:

```
repository-root/
├── widget-1/
│   ├── default/
│   │   └── program/
│   │       └── config files
│   ├── hyprland/
│   │   └── program/
│   │       └── config files
│   └── labwc/
│       └── program/
│           └── config files
└── widget-2/
    └── default/
        └── program/
            └── config files
```

## Workflow Examples

### 1. Adding a New Repository

```bash
# Add a repository to the compatible list (name automatically extracted)
python3 dotfile_manager.py <repo-path> --add-repo "https://github.com/user/my-theme.git" "My awesome theme" --filter-tags "hyprland,eww,theme"

# Add with custom name
python3 dotfile_manager.py <repo-path> --add-repo "https://github.com/user/my-theme.git" "My awesome theme" "my-custom-name"

# List to verify it was added
python3 dotfile_manager.py <repo-path> --list-repos
```

### 2. Installing from a Repository

```bash
# First, check what widgets are available
python3 dotfile_manager.py <repo-path> --install-from-git "my-theme" --dry-run

# Install all widgets from the repository
python3 dotfile_manager.py <repo-path> --install-from-git "my-theme"

# Or install just a specific widget
python3 dotfile_manager.py <repo-path> --install-from-git "my-theme" --git-widget "awesome-bar"
```

### 3. Updating Repositories

```bash
# Update and install from a repository
python3 dotfile_manager.py <repo-path> --install-from-git "my-theme" --force-update
```

### 4. Filtering by Tags

```bash
# List only Hyprland-related repositories
python3 dotfile_manager.py <repo-path> --list-repos --filter-tags "hyprland"

# List only theme repositories
python3 dotfile_manager.py <repo-path> --list-repos --filter-tags "theme"
```

## Local Repository Management

The dotfile manager creates a `git_repos/` directory in your repository root to store cloned repositories:

```
<repo-path>/
├── git_repos/
│   ├── catppuccin-hyprland/
│   ├── awesome-eww/
│   └── minimal-labwc/
├── compatible_repos.txt
└── dotfile_config.json
```

## Compatibility Checking

Before installing from a repository, the system automatically checks:

1. **Structure Compliance**: Ensures the repository follows the expected directory structure
2. **Widget Detection**: Identifies available widgets
3. **Environment Support**: Detects supported environments (hyprland, labwc, etc.)
4. **Program Support**: Identifies supported programs (eww, alacritty, etc.)

## Best Practices

### For Repository Maintainers

1. **Follow the Structure**: Use the standard directory structure with environment-specific configs
2. **Include Defaults**: Always provide a `default/` directory as fallback
3. **Document Tags**: Use meaningful tags to help users find your repository
4. **Test Compatibility**: Use the compatibility checker before publishing

### For Users

1. **Check Compatibility**: Always verify compatibility before adding repositories
2. **Use Tags**: Filter repositories by tags to find relevant ones
3. **Backup First**: The system backs up existing configs, but it's good practice to backup manually too
4. **Test with Dry Run**: Use `--dry-run` to preview changes before applying

## Troubleshooting

### Common Issues

1. **Repository Not Found**: Ensure the repository is in your compatible list
2. **Clone Failed**: Check network connection and repository URL
3. **Compatibility Issues**: Use `--check-compatibility` to diagnose structure problems
4. **Permission Denied**: Ensure you have write permissions to the repository directory

### Debug Commands

```bash
# Check what would be installed
python3 dotfile_manager.py <repo-path> --install-from-git "repo-name" --dry-run

# Check repository compatibility
python3 dotfile_manager.py <repo-path> --check-compatibility "/path/to/repo"

# List available widgets in a repository
python3 dotfile_manager.py <repo-path> --install-from-git "repo-name" --dry-run
```

## Example Repository List

Here's an example of a well-organized repository list:

```
# Popular Themes
catppuccin-hyprland|https://github.com/catppuccin/hyprland.git|Catppuccin theme for Hyprland|hyprland,theme,catppuccin
dracula-terminal|https://github.com/dracula/terminal.git|Dracula theme for terminals|terminal,theme,dracula
nord-theme|https://github.com/nordtheme/nord.git|Nord color scheme|theme,nord,universal

# Widget Collections
awesome-eww|https://github.com/awesome-eww/awesome-eww.git|Awesome EWW widgets collection|eww,widgets,awesome
minimal-widgets|https://github.com/minimal-widgets/minimal.git|Minimal widget collection|eww,widgets,minimal

# Window Manager Configs
minimal-labwc|https://github.com/minimal-labwc/minimal-labwc.git|Minimal LabWC configuration|labwc,minimal,clean
hyprland-rice|https://github.com/hyprland-rice/rice.git|Beautiful Hyprland rice|hyprland,rice,beautiful
```

This system makes it easy to discover, manage, and install dotfile configurations from the community while maintaining compatibility with your system environment.

