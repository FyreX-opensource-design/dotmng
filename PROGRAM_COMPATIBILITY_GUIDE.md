# Program Compatibility Guide

The dotfile manager includes intelligent program compatibility checking to warn users about programs that can only load one configuration file and provide helpful suggestions for handling multiple configurations.

## The Problem

Some programs like Kitty, Alacritty, and Picom can only load one configuration file and don't support command-line arguments to select between different configs. When you have multiple environment-specific configurations for these programs, they will overwrite each other, causing conflicts.

## The Solution

The dotfile manager automatically detects these compatibility issues and provides:

- **Warning messages** for programs that can't handle multiple configs
- **Helpful suggestions** for resolving conflicts
- **Detailed information** about which files are conflicting
- **Proactive checking** before installation

## Supported Program Categories

### Single Configuration Programs ⚠️

These programs can only load one configuration file:

| Program | Description | Conflict Behavior |
|---------|-------------|-------------------|
| **Kitty** | Terminal emulator | Multiple configs overwrite each other |
| **Alacritty** | Terminal emulator | Multiple configs overwrite each other |
| **st** | Simple terminal | Multiple configs overwrite each other |
| **urxvt** | Terminal emulator | Multiple configs overwrite each other |
| **Picom** | Compositor | Multiple configs overwrite each other |
| **Compton** | Compositor | Multiple configs overwrite each other |

### Multiple Configuration Programs ✅

These programs support multiple configuration files:

| Program | Description | How to Use Multiple Configs |
|---------|-------------|----------------------------|
| **EWW** | Widget system | Use `--config` flag to specify different config files |
| **Fabric** | Widget system | Use `--config` flag to specify different config files |
| **Weld** | Widget system | Use `--config` flag to specify different config files |
| **Waybar** | Status bar | Use `--config` flag to specify different config files |
| **Hyprland** | Window manager | Use `--config` flag to specify different config files |
| **LabWC** | Window manager | Use `--config` flag to specify different config files |

## Usage Examples

### Check Compatibility Before Installation

```bash
# Check program compatibility for a specific widget
python3 dotfile_manager.py <repo-path> --check-program-compatibility "<widget-name>"

# Check with environment override
python3 dotfile_manager.py <repo-path> --check-program-compatibility "<widget-name>" --environment '{"window_manager": "hyprland"}'
```

### Installation with Warnings

```bash
# Install widget (warnings shown during installation)
python3 dotfile_manager.py <repo-path> --widget "<widget-name>"

# Dry run to see warnings without installing
python3 dotfile_manager.py <repo-path> --widget "<widget-name>" --dry-run
```

## Example Output

### Compatibility Warning

```
⚠️  COMPATIBILITY WARNINGS:
   ⚠️  KITTY: Kitty can only load one configuration file. Multiple configs will overwrite each other.
      💡 Suggestion: Consider using different config names or environment-specific subdirectories.
      Conflicting files:
        - hyprland: kitty.conf
        - default: kitty.conf
```

### Compatibility Information

```
ℹ️  COMPATIBILITY INFORMATION:
   ℹ️  EWW: EWW supports multiple configuration files and can load them via command line arguments.
      💡 Suggestion: Use --config flag to specify different config files.
```

## Best Practices

### For Repository Maintainers

1. **Avoid Multiple Configs for Single-Config Programs**:
   - Use different file names: `kitty-hyprland.conf`, `kitty-default.conf`
   - Use subdirectories: `kitty/hyprland/`, `kitty/default/`
   - Provide installation scripts that handle the selection

2. **Document Configuration Selection**:
   - Include README instructions for manual config selection
   - Provide wrapper scripts for different environments
   - Use symbolic links for easy switching

3. **Use Multi-Config Programs When Possible**:
   - Prefer EWW, Waybar, or other programs that support `--config`
   - This allows true environment-specific configurations

### For Users

1. **Check Compatibility First**:
   ```bash
   python3 dotfile_manager.py <repo-path> --check-program-compatibility "<widget-name>"
   ```

2. **Review Warnings Carefully**:
   - Understand which programs will have conflicts
   - Consider if you need all the conflicting configurations
   - Look for alternative solutions

3. **Manual Configuration Management**:
   - For single-config programs, manually select the appropriate config
   - Use symbolic links to switch between configurations
   - Create wrapper scripts for different environments

## Configuration

The program compatibility settings are stored in a separate external file: `program_compatibility.json`

```json
{
  "single_config_only": {
    "kitty": {
      "warning": "Kitty can only load one configuration file. Multiple configs will overwrite each other.",
      "suggestion": "Consider using different config names or environment-specific subdirectories.",
      "category": "terminal",
      "description": "Fast, feature-rich terminal emulator"
    }
  },
  "supports_multiple_configs": {
    "eww": {
      "info": "EWW supports multiple configuration files and can load them via command line arguments.",
      "suggestion": "Use --config flag to specify different config files.",
      "category": "widget",
      "description": "ElKowars wacky widgets"
    }
  },
  "metadata": {
    "version": "1.0.0",
    "last_updated": "2024-01-01",
    "description": "Program compatibility settings for dotfile manager"
  }
}
```

### Managing the Compatibility File

```bash
# List all programs and their compatibility status
python3 dotfile_manager.py <repo-path> --list-compatible-programs

# Update from local file
python3 dotfile_manager.py <repo-path> --update-compatibility /path/to/compatibility.json

# Update from remote URL
python3 dotfile_manager.py <repo-path> --update-compatibility https://example.com/compatibility.json
```

## Workarounds for Single-Config Programs

### 1. Different File Names

```
widget/
├── default/
│   └── kitty/
│       └── kitty-default.conf
└── hyprland/
    └── kitty/
        └── kitty-hyprland.conf
```

### 2. Subdirectory Structure

```
widget/
├── default/
│   └── kitty/
│       └── default/
│           └── kitty.conf
└── hyprland/
    └── kitty/
        └── hyprland/
            └── kitty.conf
```

### 3. Installation Scripts

Create scripts that handle configuration selection:

```bash
#!/bin/bash
# install-kitty-config.sh

if [ "$XDG_CURRENT_DESKTOP" = "Hyprland" ]; then
    cp kitty-hyprland.conf ~/.config/kitty/kitty.conf
else
    cp kitty-default.conf ~/.config/kitty/kitty.conf
fi
```

### 4. Symbolic Links

```bash
# Create symlink to current environment's config
ln -sf ~/.config/kitty/kitty-hyprland.conf ~/.config/kitty/kitty.conf
```

## Troubleshooting

### Common Issues

1. **Warnings Not Showing**: Ensure the configuration file includes program compatibility settings
2. **False Positives**: Some programs might support multiple configs but aren't documented
3. **Missing Programs**: Add new programs to the compatibility configuration

### Adding New Programs

To add support for new programs, update the configuration file:

```json
{
  "program_compatibility": {
    "single_config_only": {
      "new-program": {
        "warning": "New Program can only load one configuration file.",
        "suggestion": "Use different file names or subdirectories."
      }
    }
  }
}
```

## Benefits

- **Prevents Configuration Conflicts**: Warns before problems occur
- **Educates Users**: Explains program limitations and solutions
- **Improves User Experience**: Provides clear guidance and suggestions
- **Reduces Support Issues**: Proactive problem detection
- **Encourages Best Practices**: Guides users toward better solutions

This compatibility system helps users make informed decisions about their dotfile configurations and avoid common pitfalls with programs that have limited configuration flexibility.
