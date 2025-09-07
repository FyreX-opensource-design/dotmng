# Demo Scripts Overview

This directory contains several demo scripts that showcase different features of the dotfile manager.

## Available Demo Scripts

### Core Features
- **`simplified_mapping_demo.sh`** - Demonstrates the simplified file mapping system
  - Shows automatic folder-to-config mapping
  - Explains benefits of the simplified approach
  - Compares before/after configuration
- **`environment_detection_demo.sh`** - Enhanced environment detection system
  - Shows environment variable-based detection
  - Demonstrates detection priority and fallbacks
  - Explains supported environment variables
- **`folder_structure_demo.sh`** - Folder structure environment detection
  - Shows how folder structure automatically handles environment detection
  - Demonstrates the elimination of hardcoded environment lists
  - Explains the intuitive folder-based approach
- **`config_management_demo.sh`** - Configuration management features
  - Shows pulling configurations from ~/.config to repository structure
  - Demonstrates using ~/.config as fallback during installation
  - Explains bidirectional configuration management

### Git Repository Features
- **`git_demo.sh`** - Git repository management features
  - Pulling repositories from Git
  - Repository compatibility checking
  - Managing compatible repositories list

### Metadata and Filtering
- **`metadata_demo.sh`** - Metadata extraction and tag filtering
  - Automatic description and tag extraction
  - Tag-based repository filtering
  - Repository information display

### URL Handling
- **`url_demo.sh`** - URL-based repository handling
  - Direct URL repository processing
  - URL validation and processing
  - Repository information extraction from URLs

### Compatibility System
- **`external_compatibility_demo.sh`** - External compatibility file system
  - External program compatibility database
  - Compatibility warnings and suggestions
  - Environment-aware compatibility checking

## Usage

All demo scripts are executable and can be run directly:

```bash
# Make scripts executable (if needed)
chmod +x *.sh

# Run any demo
./simplified_mapping_demo.sh
./environment_detection_demo.sh
./folder_structure_demo.sh
./config_management_demo.sh
./git_demo.sh
./metadata_demo.sh
./url_demo.sh
./external_compatibility_demo.sh
```

## Demo Script Features

Each demo script:
- ✅ Uses the example repository structure
- ✅ Demonstrates specific features clearly
- ✅ Provides educational output and explanations
- ✅ Shows real-world usage examples
- ✅ Includes error handling and validation

## Cleanup Notes

The following obsolete demo scripts have been removed:
- ~~`demo.sh`~~ - Basic demo (superseded by more specific demos)
- ~~`complete_demo.sh`~~ - Overly comprehensive demo
- ~~`compatibility_demo.sh`~~ - Superseded by `external_compatibility_demo.sh`

The remaining demos focus on specific features and provide clear, focused demonstrations of the dotfile manager's capabilities.
