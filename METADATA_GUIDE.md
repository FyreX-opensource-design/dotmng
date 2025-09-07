# Repository Metadata Guide

The dotfile manager can automatically fetch descriptions and tags from metadata files in repositories, making them self-documenting and eliminating the need to manually specify this information.

## Supported Metadata File Formats

The system looks for metadata files in the following order:

1. **`dotfile-info.json`** - JSON format (recommended)
2. **`dotfile-info.yaml`** - YAML format
3. **`dotfile-info.yml`** - YAML format (alternative extension)
4. **`.dotfile-info.json`** - Hidden JSON file
5. **`README.md`** - Basic extraction from markdown

## JSON Format (Recommended)

Create a `dotfile-info.json` file in your repository root:

```json
{
  "description": "A beautiful Hyprland configuration with EWW widgets",
  "tags": ["hyprland", "eww", "theme", "minimal"],
  "author": "Your Name",
  "version": "1.0.0",
  "compatibility": ["hyprland", "labwc", "sway"],
  "programs": ["eww", "alacritty", "picom"],
  "license": "MIT",
  "homepage": "https://github.com/yourusername/your-repo",
  "documentation": "README.md"
}
```

## YAML Format

Create a `dotfile-info.yaml` file in your repository root:

```yaml
description: "A beautiful Hyprland configuration with EWW widgets"
tags:
  - hyprland
  - eww
  - theme
  - minimal
author: "Your Name"
version: "1.0.0"
compatibility:
  - hyprland
  - labwc
  - sway
programs:
  - eww
  - alacritty
  - picom
license: "MIT"
homepage: "https://github.com/yourusername/your-repo"
documentation: "README.md"
```

## Supported Metadata Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `description` | string | Repository description | No |
| `tags` | array | List of tags for categorization | No |
| `author` | string | Repository author/maintainer | No |
| `version` | string | Version information | No |
| `compatibility` | array | Supported environments | No |
| `programs` | array | Supported programs | No |
| `license` | string | License information | No |
| `homepage` | string | Project homepage URL | No |
| `documentation` | string | Documentation file path | No |

## README.md Fallback

If no dedicated metadata files are found, the system will attempt to extract basic information from `README.md`:

- **Description**: First `# Title` line
- **Tags**: Any `#tag` patterns found in the content

## Usage Examples

### Automatic Metadata Fetching

```bash
# Add repository with automatic metadata fetching
python3 dotfile_manager.py <repo-path> --add-repo "https://github.com/user/repo.git"

# The system will automatically:
# 1. Clone the repository temporarily
# 2. Look for metadata files
# 3. Extract description and tags
# 4. Add to repository list with fetched metadata
```

### Manual Override

```bash
# Add repository without fetching metadata
python3 dotfile_manager.py <repo-path> --add-repo "https://github.com/user/repo.git" "Manual description" --no-fetch-metadata

# Add with custom tags
python3 dotfile_manager.py <repo-path> --add-repo "https://github.com/user/repo.git" "Description" --filter-tags "custom,tags"
```

### Local Repository Testing

```bash
# Test metadata fetching on local repository
python3 dotfile_manager.py <repo-path> --add-repo "/path/to/local/repo"

# Test with file:// URL
python3 dotfile_manager.py <repo-path> --add-repo "file:///path/to/local/repo"
```

## Best Practices for Repository Maintainers

### 1. Create a Metadata File

Always include a `dotfile-info.json` file in your repository root:

```json
{
  "description": "Clear, concise description of your dotfiles",
  "tags": ["hyprland", "eww", "theme", "minimal"],
  "author": "Your Name",
  "version": "1.0.0",
  "compatibility": ["hyprland", "labwc"],
  "programs": ["eww", "alacritty"],
  "license": "MIT"
}
```

### 2. Use Meaningful Tags

Choose tags that help users find your repository:

- **Environment tags**: `hyprland`, `labwc`, `sway`, `i3`
- **Program tags**: `eww`, `alacritty`, `kitty`, `picom`
- **Style tags**: `minimal`, `colorful`, `dark`, `light`
- **Category tags**: `theme`, `widgets`, `config`, `rice`

### 3. Keep Descriptions Concise

- Keep descriptions under 100 characters
- Focus on what makes your configuration unique
- Mention key features or programs

### 4. Update Version Information

- Increment version numbers when making significant changes
- Use semantic versioning (e.g., `1.0.0`, `1.1.0`, `2.0.0`)

## Example Repository Structure

```
my-awesome-dotfiles/
├── dotfile-info.json          # Metadata file
├── README.md                  # Documentation
├── awesome-widget/
│   ├── default/
│   │   └── eww/
│   │       └── config.eww
│   ├── hyprland/
│   │   └── eww/
│   │       └── config.eww
│   └── labwc/
│       └── eww/
│           └── config.eww
└── terminal-theme/
    └── default/
        └── alacritty/
            └── alacritty.toml
```

## Troubleshooting

### Common Issues

1. **Metadata not found**: Ensure the metadata file is in the repository root
2. **JSON parsing errors**: Validate your JSON syntax
3. **YAML not supported**: Install PyYAML or use JSON format
4. **Local path issues**: Use absolute paths for local repositories

### Debug Commands

```bash
# Check if metadata is being fetched
python3 dotfile_manager.py <repo-path> --add-repo "https://github.com/user/repo.git" --dry-run

# Test local repository
python3 dotfile_manager.py <repo-path> --add-repo "/path/to/repo"

# Disable metadata fetching for testing
python3 dotfile_manager.py <repo-path> --add-repo "https://github.com/user/repo.git" --no-fetch-metadata
```

## Benefits

- **Self-Documenting**: Repositories describe themselves
- **Consistent**: Standardized metadata format
- **Discoverable**: Better search and filtering
- **Maintainable**: Metadata stays with the code
- **Automatic**: No manual entry required

This system makes it easy for users to discover and understand repositories while reducing the maintenance burden on repository maintainers.
