#!/usr/bin/env python3
"""
Dotfile Manager - A flexible dotfile management system

This script manages dotfiles based on system environment detection,
supporting hierarchical configuration selection with fallbacks.
"""

import os
import sys
import shutil
import argparse
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
import urllib.parse
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class DotfileManager:
    """Main dotfile manager class"""
    
    def __init__(self, repo_path: str, config_file: str = "dotfile_config.json"):
        self.repo_path = Path(repo_path).resolve()
        self.home_config = Path.home() / ".config"
        self.config_file = self.repo_path / config_file
        self.config = self._load_config()
        # Look for configuration files in priority order: script dir -> repo path -> ~/.config
        script_dir = Path(__file__).parent
        self.repo_list_file = script_dir / "compatible_repos.txt"
        if not self.repo_list_file.exists():
            self.repo_list_file = self.repo_path / "compatible_repos.txt"
        if not self.repo_list_file.exists():
            self.repo_list_file = self.home_config / "compatible_repos.txt"
        
        self.git_repos_dir = self.repo_path / "git_repos"
        
        self.program_compatibility_file = script_dir / "program_compatibility.json"
        if not self.program_compatibility_file.exists():
            self.program_compatibility_file = self.repo_path / "program_compatibility.json"
        if not self.program_compatibility_file.exists():
            self.program_compatibility_file = self.home_config / "program_compatibility.json"
        self.program_compatibility = self._load_program_compatibility()
        
        # Load auto config rules
        self.auto_config_rules_file = script_dir / "auto_config_rules.json"
        if not self.auto_config_rules_file.exists():
            self.auto_config_rules_file = self.repo_path / "auto_config_rules.json"
        if not self.auto_config_rules_file.exists():
            self.auto_config_rules_file = self.home_config / "auto_config_rules.json"
        self.auto_config_rules = self._load_auto_config_rules()
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        # Check primary config file location
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing config file: {e}")
                return self._get_default_config()
        
        # Fallback to ~/.config
        fallback_config = self.home_config / self.config_file.name
        if fallback_config.exists():
            try:
                logger.info(f"Using config file from ~/.config: {fallback_config}")
                with open(fallback_config, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing fallback config file: {e}")
                return self._get_default_config()
        
        logger.info("No config file found, using defaults")
        return self._get_default_config()
    
    def _load_program_compatibility(self) -> Dict:
        """Load program compatibility settings from external file"""
        if self.program_compatibility_file.exists():
            try:
                logger.info(f"Loading program compatibility from: {self.program_compatibility_file}")
                with open(self.program_compatibility_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing program compatibility file: {e}")
                return self._get_default_program_compatibility()
        else:
            logger.info("No program compatibility file found, using defaults")
            return self._get_default_program_compatibility()
    
    def _load_auto_config_rules(self) -> Dict:
        """Load auto configuration filtering rules from external file"""
        if self.auto_config_rules_file.exists():
            try:
                logger.info(f"Loading auto config rules from: {self.auto_config_rules_file}")
                with open(self.auto_config_rules_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing auto config rules file: {e}")
                return self._get_default_auto_config_rules()
        else:
            logger.info("No auto config rules file found, using defaults")
            return self._get_default_auto_config_rules()
    
    def _get_default_auto_config_rules(self) -> Dict:
        """Get default auto configuration filtering rules"""
        return {
            "include_programs": {
                "terminals": ["alacritty", "kitty", "st", "urxvt", "xterm"],
                "window_managers": ["dwm", "i3", "sway", "hyprland", "labwc"],
                "bars_widgets": ["eww", "waybar", "polybar", "fabric", "weld"],
                "compositors": ["picom", "compton", "xcompmgr"],
                "editors": ["vim", "nvim", "emacs"],
                "shells": ["zsh", "bash", "fish"],
                "other": ["tmux", "git", "ssh"]
            },
            "exclude_directories": {
                "system": ["systemd", "dconf", "kde.org", "KDE", "pulse", "gtk-3.0", "gtk-4.0"],
                "browsers": ["chromium", "firefox", "chrome"],
                "applications": ["rustdesk", "antimicrox", "opendeck", "nemo", "gtklock"]
            },
            "include_keywords": ["wm", "bar", "term", "editor", "shell", "compositor"],
            "ignore_patterns": ["*.lock", "*.socket", "*.cookie", "*.pid", "*.tmp", "*.log", "*.cache"],
            "confirmation_threshold": 10,
            "max_configs_per_pull": 50
        }
    
    def _get_default_program_compatibility(self) -> Dict:
        """Get default program compatibility settings"""
        return {
            "single_config_only": {
                "alacritty": {
                    "warning": "Alacritty can only load one configuration file. Multiple configs will overwrite each other.",
                    "suggestion": "Consider using different config names or environment-specific subdirectories."
                },
                "kitty": {
                    "warning": "Kitty can only load one configuration file. Multiple configs will overwrite each other.",
                    "suggestion": "Consider using different config names or environment-specific subdirectories."
                }
            },
            "supports_multiple_configs": {
                "eww": {
                    "info": "EWW supports multiple configuration files and can load them via command line arguments.",
                    "suggestion": "Use --config flag to specify different config files."
                }
            }
        }
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            "backup_existing": True,
            "create_backup_dir": True,
            "dry_run": False
        }
    
    def detect_environment(self) -> Dict[str, str]:
        """Detect current system environment"""
        env = {}
        
        # Detect window manager
        wm = self._detect_window_manager()
        if wm:
            env['window_manager'] = wm
        
        # Detect compositor
        compositor = self._detect_compositor()
        if compositor:
            env['compositor'] = compositor
            
        # Detect shell
        shell = os.environ.get('SHELL', '').split('/')[-1]
        if shell:
            env['shell'] = shell
            
        # Detect terminal
        terminal = os.environ.get('TERM', '')
        if terminal:
            env['terminal'] = terminal
            
        logger.info(f"Detected environment: {env}")
        return env
    
    def _detect_window_manager(self) -> Optional[str]:
        """Detect current window manager"""
        # Check for Hyprland
        if os.environ.get('HYPRLAND_INSTANCE_SIGNATURE'):
            return 'hyprland'
        
        # Check for LabWC
        if os.environ.get('LABWC_SOCKET'):
            return 'labwc'
            
        # Check for Sway
        if os.environ.get('SWAYSOCK'):
            return 'sway'
            
        # Check for i3
        if os.environ.get('I3SOCK'):
            return 'i3'
        
        # Check DESKTOP_SESSION environment variable
        desktop_session = os.environ.get('DESKTOP_SESSION', '').lower()
        if desktop_session in ['hyprland', 'labwc', 'sway', 'i3', 'openbox', 'fluxbox']:
            return desktop_session
        
        # Check XDG_CURRENT_DESKTOP environment variable
        xdg_desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
        if 'hyprland' in xdg_desktop:
            return 'hyprland'
        elif 'labwc' in xdg_desktop:
            return 'labwc'
        elif 'sway' in xdg_desktop:
            return 'sway'
        elif 'i3' in xdg_desktop:
            return 'i3'
        elif 'openbox' in xdg_desktop:
            return 'openbox'
        elif 'fluxbox' in xdg_desktop:
            return 'fluxbox'
            
        # Try to detect via ps
        try:
            result = subprocess.run(['ps', '-e'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'hyprland' in line.lower():
                    return 'hyprland'
                elif 'labwc' in line.lower():
                    return 'labwc'
                elif 'sway' in line.lower():
                    return 'sway'
                elif 'i3' in line.lower():
                    return 'i3'
        except:
            pass
            
        return None
    
    def _detect_compositor(self) -> Optional[str]:
        """Detect current compositor"""
        # Check for Wayland (Wayland has built-in compositing)
        if os.environ.get('WAYLAND_DISPLAY'):
            return 'wayland'
        
        # Check for X11 compositor environment variables
        if os.environ.get('PICOM_CONFIG'):
            return 'picom'
        
        # Check for X11 session type
        session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
        if session_type == 'wayland':
            return 'wayland'
        
        # Fallback to process detection
        try:
            result = subprocess.run(['ps', '-e'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'picom' in line.lower():
                    return 'picom'
                elif 'compton' in line.lower():
                    return 'compton'
                elif 'xcompmgr' in line.lower():
                    return 'xcompmgr'
        except:
            pass
            
        return None
    
    def find_widget_configs(self, widget_name: str) -> List[Path]:
        """Find all configuration directories for a widget"""
        widget_path = self.repo_path / widget_name
        if not widget_path.exists():
            logger.warning(f"Widget '{widget_name}' not found in {self.repo_path}")
            return []
        
        configs = []
        
        # Look for environment-specific configs
        for item in widget_path.iterdir():
            if item.is_dir() and item.name != 'default':
                configs.append(item)
        
        # Add default config if it exists
        default_path = widget_path / 'default'
        if default_path.exists():
            configs.append(default_path)
            
        return configs
    
    def select_best_config(self, widget_name: str, environment: Dict[str, str]) -> Optional[Path]:
        """Select the best configuration based on environment"""
        configs = self.find_widget_configs(widget_name)
        if not configs:
            return None
        
        # Priority order: exact match > partial match > default
        best_config = None
        best_score = 0
        
        for config_path in configs:
            if config_path.name == 'default':
                continue
                
            score = 0
            config_name = config_path.name.lower()
            
            # Check for exact matches
            for env_type, env_value in environment.items():
                if env_value and env_value.lower() in config_name:
                    score += 2
            
            # Check for partial matches
            for env_type, env_value in environment.items():
                if env_value and any(part in config_name for part in env_value.lower().split()):
                    score += 1
            
            if score > best_score:
                best_score = score
                best_config = config_path
        
        # Fallback to default if no good match found
        if not best_config:
            default_path = self.repo_path / widget_name / 'default'
            if default_path.exists():
                best_config = default_path
        
        return best_config
    
    def get_config_files(self, config_path: Path) -> List[Tuple[Path, str]]:
        """Get all config files from a configuration directory"""
        files = []
        
        for item in config_path.rglob('*'):
            if item.is_file() and not item.name.startswith('.'):
                # Determine target directory based on file location
                relative_path = item.relative_to(config_path)
                
                # Check if it's in a specific program directory
                if len(relative_path.parts) > 1:
                    program_name = relative_path.parts[0]
                    # Check for custom mappings first
                    widget_name = config_path.parent.name
                    custom_mappings = self.config.get('custom_mappings', {}).get(widget_name, {})
                    if program_name in custom_mappings:
                        target_dir = self.home_config / custom_mappings[program_name]
                    else:
                        # Use folder name directly as the target directory
                        target_dir = self.home_config / program_name
                else:
                    # Use filename as the target directory
                    program_name = item.stem
                    target_dir = self.home_config / program_name
                
                files.append((item, str(target_dir)))
        
        return files
    
    def check_program_compatibility(self, config_files: List[Tuple[Path, str]], widget_name: str = None) -> Dict[str, List[str]]:
        """Check for program compatibility issues and return warnings"""
        warnings = {
            'single_config_warnings': [],
            'multiple_config_info': []
        }
        
        # Group files by program
        program_files = {}
        for source_path, target_dir in config_files:
            program_name = Path(target_dir).name
            if program_name not in program_files:
                program_files[program_name] = []
            program_files[program_name].append((source_path, target_dir))
        
        # If widget_name is provided, check across all environments for that widget
        if widget_name:
            all_configs = self.find_widget_configs(widget_name)
            all_program_files = {}
            
            for config_path in all_configs:
                all_files = self.get_config_files(config_path)
                for source_path, target_dir in all_files:
                    program_name = Path(target_dir).name
                    if program_name not in all_program_files:
                        all_program_files[program_name] = []
                    all_program_files[program_name].append((source_path, target_dir))
            
            # Use the comprehensive list if we have multiple environments
            if len(all_configs) > 1:
                program_files = all_program_files
        
        # Check each program for compatibility issues
        single_config_programs = self.program_compatibility.get('single_config_only', {})
        multiple_config_programs = self.program_compatibility.get('supports_multiple_configs', {})
        
        for program_name, files in program_files.items():
            if len(files) > 1:  # Multiple configs for the same program
                if program_name in single_config_programs:
                    # Warning for single-config programs
                    warning_info = single_config_programs[program_name]
                    warning_msg = f"⚠️  {program_name.upper()}: {warning_info['warning']}"
                    suggestion_msg = f"   💡 Suggestion: {warning_info['suggestion']}"
                    warnings['single_config_warnings'].extend([warning_msg, suggestion_msg])
                    
                    # Add details about conflicting files
                    file_details = []
                    for source_path, target_dir in files:
                        env_name = source_path.parent.parent.name
                        file_details.append(f"     - {env_name}: {source_path.name}")
                    if file_details:
                        warnings['single_config_warnings'].append("   Conflicting files:")
                        warnings['single_config_warnings'].extend(file_details)
                        
                elif program_name in multiple_config_programs:
                    # Info for multi-config programs
                    info_data = multiple_config_programs[program_name]
                    info_msg = f"ℹ️  {program_name.upper()}: {info_data['info']}"
                    suggestion_msg = f"   💡 Suggestion: {info_data['suggestion']}"
                    warnings['multiple_config_info'].extend([info_msg, suggestion_msg])
        
        return warnings
    
    def backup_existing(self, target_path: Path) -> bool:
        """Backup existing configuration file"""
        if not target_path.exists():
            return True
            
        if not self.config.get('backup_existing', True):
            return True
        
        backup_dir = Path.home() / ".config_backup"
        if self.config.get('create_backup_dir', True):
            backup_dir.mkdir(exist_ok=True)
        
        backup_path = backup_dir / target_path.name
        counter = 1
        while backup_path.exists():
            backup_path = backup_dir / f"{target_path.name}.{counter}"
            counter += 1
        
        try:
            shutil.copy2(target_path, backup_path)
            logger.info(f"Backed up {target_path} to {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to backup {target_path}: {e}")
            return False
    
    def install_config(self, source_path: Path, target_dir: str) -> bool:
        """Install a configuration file"""
        target_path = Path(target_dir) / source_path.name
        
        if self.config.get('dry_run', False):
            logger.info(f"[DRY RUN] Would copy {source_path} to {target_path}")
            return True
        
        # Create target directory
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Backup existing file
        if not self.backup_existing(target_path):
            return False
        
        try:
            shutil.copy2(source_path, target_path)
            logger.info(f"Installed {source_path} to {target_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to install {source_path} to {target_path}: {e}")
            return False
    
    def pull_from_config(self, widget_name: str, environment: Optional[str] = None, 
                        specific_programs: Optional[List[str]] = None, 
                        output_dir: Optional[str] = None) -> bool:
        """Pull existing configurations from ~/.config to specified directory"""
        try:
            # Use custom output directory if provided, otherwise use repo structure
            if output_dir:
                base_path = Path(output_dir).resolve()
                widget_path = base_path / widget_name
            else:
                widget_path = self.repo_path / widget_name
            
            if not widget_path.exists():
                widget_path.mkdir(parents=True, exist_ok=True)
            
            # Determine target environment folder
            if environment:
                env_folder = widget_path / environment
            else:
                # Use detected environment
                detected_env = self.detect_environment()
                env_name = detected_env.get('window_manager', 'default')
                env_folder = widget_path / env_name
            
            env_folder.mkdir(parents=True, exist_ok=True)
            
            # Get configuration from external file
            include_programs = self.auto_config_rules.get('include_programs', {})
            exclude_directories = self.auto_config_rules.get('exclude_directories', {})
            include_keywords = self.auto_config_rules.get('include_keywords', [])
            confirmation_threshold = self.auto_config_rules.get('confirmation_threshold', 10)
            max_configs = self.auto_config_rules.get('max_configs_per_pull', 50)
            
            # Flatten include programs into a single set
            common_dotfile_programs = set()
            for category, programs in include_programs.items():
                common_dotfile_programs.update(programs)
            
            # Flatten exclude directories into a single set
            exclude_dirs = set()
            for category, directories in exclude_directories.items():
                exclude_dirs.update(directories)
            
            # Get list of config directories
            if specific_programs:
                # Only pull specified programs
                config_dirs = []
                for program in specific_programs:
                    program_path = self.home_config / program
                    if program_path.exists() and program_path.is_dir():
                        config_dirs.append(program_path)
            else:
                # Pull common dotfile programs, excluding system directories
                config_dirs = []
                for item in self.home_config.iterdir():
                    if (item.is_dir() and 
                        not item.name.startswith('.') and
                        item.name not in exclude_dirs and
                        (item.name in common_dotfile_programs or 
                         any(keyword in item.name.lower() for keyword in include_keywords))):
                        config_dirs.append(item)
            
            if not config_dirs:
                print(f"No suitable configurations found in {self.home_config}")
                print("Tip: Use --specific-programs to specify which programs to pull")
                return False
            
            print(f"Pulling configurations from {self.home_config} to {env_folder}")
            print(f"Found {len(config_dirs)} suitable configurations:")
            
            # Check if we exceed the maximum configs limit
            if len(config_dirs) > max_configs:
                print(f"Too many configurations found ({len(config_dirs)}). Maximum allowed: {max_configs}")
                print("Tip: Use --specific-programs to limit which programs to pull")
                return False
            
            # Ask for confirmation if pulling many configs
            if len(config_dirs) > confirmation_threshold:
                response = input(f"About to pull {len(config_dirs)} configurations. Continue? (y/N): ")
                if response.lower() != 'y':
                    print("Operation cancelled.")
                    return False
            
            for config_dir in config_dirs:
                target_dir = env_folder / config_dir.name
                print(f"  - {config_dir.name} -> {target_dir}")
                
                # Copy the config directory with better filtering
                if target_dir.exists():
                    import shutil
                    shutil.rmtree(target_dir)
                
                import shutil
                try:
                    # Use ignore patterns from external configuration
                    ignore_patterns_list = self.auto_config_rules.get('ignore_patterns', [
                        '*.lock', '*.socket', '*.cookie', '*.pid', '*.tmp', '*.log', '*.cache'
                    ])
                    ignore_patterns = shutil.ignore_patterns(*ignore_patterns_list)
                    shutil.copytree(config_dir, target_dir, ignore=ignore_patterns)
                except (OSError, IOError) as e:
                    print(f"    Warning: Could not copy {config_dir.name}: {e}")
                    continue
            
            print(f"Successfully pulled {len(config_dirs)} configurations to {env_folder}")
            return True
            
        except Exception as e:
            print(f"Error pulling configurations: {e}")
            return False

    def install_widget(self, widget_name: str, environment: Optional[Dict[str, str]] = None, use_config_fallback: bool = False) -> bool:
        """Install configuration for a specific widget"""
        if environment is None:
            environment = self.detect_environment()
        
        config_path = self.select_best_config(widget_name, environment)
        if not config_path:
            if use_config_fallback:
                logger.info(f"No configuration found for widget '{widget_name}', using ~/.config as fallback")
                # Use ~/.config directly as the source
                config_path = self.home_config
            else:
                logger.error(f"No suitable configuration found for widget '{widget_name}'")
                return False
        
        logger.info(f"Installing widget '{widget_name}' using config from {config_path}")
        
        config_files = self.get_config_files(config_path)
        if not config_files:
            logger.warning(f"No configuration files found in {config_path}")
            return False
        
        # Check for program compatibility issues
        compatibility_warnings = self.check_program_compatibility(config_files, widget_name)
        
        if compatibility_warnings['single_config_warnings']:
            logger.warning("Program compatibility warnings detected:")
            for warning in compatibility_warnings['single_config_warnings']:
                logger.warning(warning)
            print()  # Add blank line for readability
        
        if compatibility_warnings['multiple_config_info']:
            logger.info("Program compatibility information:")
            for info in compatibility_warnings['multiple_config_info']:
                logger.info(info)
            print()  # Add blank line for readability
        
        success = True
        for source_path, target_dir in config_files:
            if not self.install_config(source_path, target_dir):
                success = False
        
        return success
    
    def install_all_widgets(self, environment: Optional[Dict[str, str]] = None) -> bool:
        """Install all available widgets"""
        if environment is None:
            environment = self.detect_environment()
        
        widgets = [d.name for d in self.repo_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        if not widgets:
            logger.warning("No widgets found in repository")
            return False
        
        logger.info(f"Installing {len(widgets)} widgets: {', '.join(widgets)}")
        
        success = True
        for widget in widgets:
            if not self.install_widget(widget, environment):
                success = False
        
        return success
    
    def list_widgets(self) -> List[str]:
        """List all available widgets"""
        widgets = [d.name for d in self.repo_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        return sorted(widgets)
    
    def show_widget_info(self, widget_name: str) -> None:
        """Show information about a widget"""
        configs = self.find_widget_configs(widget_name)
        if not configs:
            print(f"Widget '{widget_name}' not found")
            return
        
        print(f"\nWidget: {widget_name}")
        print(f"Available configurations:")
        
        for config in configs:
            print(f"  - {config.name}")
            files = self.get_config_files(config)
            for source_path, target_dir in files:
                print(f"    {source_path.relative_to(self.repo_path)} -> {target_dir}")
    
    def load_repo_list(self) -> List[Dict[str, str]]:
        """Load the list of compatible repositories"""
        repos = []
        if self.repo_list_file.exists():
            try:
                with open(self.repo_list_file, 'r') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Parse format: name|url|description|tags
                            parts = line.split('|')
                            if len(parts) >= 2:
                                repo_info = {
                                    'name': parts[0].strip(),
                                    'url': parts[1].strip(),
                                    'description': parts[2].strip() if len(parts) > 2 else '',
                                    'tags': parts[3].strip().split(',') if len(parts) > 3 else [],
                                    'line_number': line_num
                                }
                                repos.append(repo_info)
                            else:
                                logger.warning(f"Invalid format in repo list line {line_num}: {line}")
            except Exception as e:
                logger.error(f"Error reading repo list: {e}")
        return repos
    
    def save_repo_list(self, repos: List[Dict[str, str]]) -> bool:
        """Save the list of compatible repositories"""
        try:
            with open(self.repo_list_file, 'w') as f:
                f.write("# Compatible Dotfile Repositories\n")
                f.write("# Format: name|url|description|tags (comma-separated)\n")
                f.write("# Example: my-theme|https://github.com/user/my-theme.git|A beautiful theme|hyprland,eww\n\n")
                
                for repo in repos:
                    tags_str = ','.join(repo.get('tags', []))
                    f.write(f"{repo['name']}|{repo['url']}|{repo.get('description', '')}|{tags_str}\n")
            return True
        except Exception as e:
            logger.error(f"Error saving repo list: {e}")
            return False
    
    def extract_repo_name_from_url(self, url: str) -> str:
        """Extract repository name from URL"""
        try:
            # Parse the URL
            parsed = urllib.parse.urlparse(url)
            
            # Handle different URL formats
            if parsed.netloc in ['github.com', 'gitlab.com', 'bitbucket.org']:
                # Extract path and remove .git suffix
                path = parsed.path.strip('/')
                if path.endswith('.git'):
                    path = path[:-4]
                
                # Split by '/' and take the last part (repo name)
                repo_name = path.split('/')[-1]
                return repo_name
            
            # For other URLs, try to extract from path
            path = parsed.path.strip('/')
            if path.endswith('.git'):
                path = path[:-4]
            
            # Take the last part of the path
            repo_name = path.split('/')[-1] if path else "unknown-repo"
            return repo_name
            
        except Exception as e:
            logger.warning(f"Could not extract repo name from URL {url}: {e}")
            return "unknown-repo"
    
    def add_repo(self, url: str, description: str = "", tags: List[str] = None, name: str = None, fetch_metadata: bool = True) -> bool:
        """Add a repository to the compatible list"""
        if tags is None:
            tags = []
        
        # Extract name from URL if not provided
        if name is None:
            name = self.extract_repo_name_from_url(url)
        
        repos = self.load_repo_list()
        
        # Check if repo already exists
        for repo in repos:
            if repo['name'] == name or repo['url'] == url:
                logger.warning(f"Repository already exists: {name}")
                return False
        
        # Try to fetch metadata from the repository if requested
        if fetch_metadata and not description and not tags:
            logger.info(f"Fetching metadata from repository: {name}")
            try:
                # Check if URL is a local path
                if url.startswith('file://') or url.startswith('/') or not url.startswith(('http', 'git@', 'ssh://')):
                    # Handle local path
                    if url.startswith('file://'):
                        local_path = Path(url[7:])  # Remove 'file://' prefix
                    else:
                        local_path = Path(url)
                    
                    if local_path.exists():
                        metadata = self.read_repo_metadata(local_path)
                    else:
                        raise FileNotFoundError(f"Local path does not exist: {local_path}")
                else:
                    # Clone the repository temporarily to read metadata
                    temp_path = self.git_repos_dir / f"temp_{name}"
                    if temp_path.exists():
                        shutil.rmtree(temp_path)
                    
                    # Clone to temp location
                    subprocess.run(['git', 'clone', url, str(temp_path)], 
                                 check=True, capture_output=True, text=True)
                    
                    # Read metadata
                    metadata = self.read_repo_metadata(temp_path)
                    
                    # Clean up temp directory
                    shutil.rmtree(temp_path)
                
                # Use metadata if available
                if metadata.get('description'):
                    description = metadata['description']
                if metadata.get('tags'):
                    tags = metadata['tags']
                
                logger.info(f"Fetched metadata: description='{description}', tags={tags}")
                
            except Exception as e:
                logger.warning(f"Could not fetch metadata from repository: {e}")
        
        new_repo = {
            'name': name,
            'url': url,
            'description': description,
            'tags': tags
        }
        
        repos.append(new_repo)
        return self.save_repo_list(repos)
    
    def add_repo_from_url(self, url: str, description: str = "", tags: List[str] = None) -> Tuple[bool, str]:
        """Add a repository from URL with automatic name extraction"""
        extracted_name = self.extract_repo_name_from_url(url)
        success = self.add_repo(url, description, tags, extracted_name)
        return success, extracted_name
    
    def remove_repo(self, name: str) -> bool:
        """Remove a repository from the compatible list"""
        repos = self.load_repo_list()
        original_count = len(repos)
        repos = [repo for repo in repos if repo['name'] != name]
        
        if len(repos) == original_count:
            logger.warning(f"Repository not found: {name}")
            return False
        
        return self.save_repo_list(repos)
    
    def read_repo_metadata(self, repo_path: Path) -> Dict[str, any]:
        """Read metadata from repository files"""
        metadata = {
            'description': '',
            'tags': [],
            'author': '',
            'version': '',
            'compatibility': [],
            'source': 'file'
        }
        
        # Try different metadata file formats
        metadata_files = [
            'dotfile-info.json',
            'dotfile-info.yaml',
            'dotfile-info.yml',
            '.dotfile-info.json',
            'README.md'
        ]
        
        for filename in metadata_files:
            file_path = repo_path / filename
            if file_path.exists():
                try:
                    if filename.endswith('.json'):
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            metadata.update(data)
                            break
                    elif filename.endswith(('.yaml', '.yml')):
                        # Try to import yaml, fall back to basic parsing if not available
                        try:
                            import yaml
                            with open(file_path, 'r') as f:
                                data = yaml.safe_load(f)
                                metadata.update(data)
                                break
                        except ImportError:
                            logger.warning("PyYAML not available, skipping YAML metadata files")
                    elif filename == 'README.md':
                        # Extract basic info from README
                        with open(file_path, 'r') as f:
                            content = f.read()
                            # Look for common patterns
                            lines = content.split('\n')
                            for line in lines[:10]:  # Check first 10 lines
                                if line.startswith('# '):
                                    metadata['description'] = line[2:].strip()
                                    break
                            # Look for tags in markdown
                            import re
                            tag_matches = re.findall(r'#(\w+)', content)
                            if tag_matches:
                                metadata['tags'] = list(set(tag_matches))
                except Exception as e:
                    logger.warning(f"Could not read metadata from {filename}: {e}")
                    continue
        
        return metadata
    
    def clone_repo(self, repo_info: Dict[str, str], force_update: bool = False) -> bool:
        """Clone or update a repository"""
        repo_name = repo_info['name']
        repo_url = repo_info['url']
        local_path = self.git_repos_dir / repo_name
        
        # Create git_repos directory if it doesn't exist
        self.git_repos_dir.mkdir(exist_ok=True)
        
        if local_path.exists():
            if force_update:
                logger.info(f"Updating repository: {repo_name}")
                try:
                    # Update existing repository
                    subprocess.run(['git', 'pull'], cwd=local_path, check=True, 
                                 capture_output=True, text=True)
                    logger.info(f"Successfully updated {repo_name}")
                    return True
                except subprocess.CalledProcessError as e:
                    logger.error(f"Failed to update {repo_name}: {e}")
                    return False
            else:
                logger.info(f"Repository {repo_name} already exists. Use --force-update to update.")
                return True
        else:
            logger.info(f"Cloning repository: {repo_name}")
            try:
                subprocess.run(['git', 'clone', repo_url, str(local_path)], 
                             check=True, capture_output=True, text=True)
                logger.info(f"Successfully cloned {repo_name}")
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to clone {repo_name}: {e}")
                return False
    
    def check_repo_compatibility(self, repo_path: Path) -> Dict[str, any]:
        """Check if a repository is compatible with our structure"""
        compatibility = {
            'is_compatible': False,
            'widgets': [],
            'environments': set(),
            'programs': set(),
            'issues': []
        }
        
        if not repo_path.exists():
            compatibility['issues'].append("Repository path does not exist")
            return compatibility
        
        # Look for widget directories
        for item in repo_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                widget_name = item.name
                compatibility['widgets'].append(widget_name)
                
                # Check for environment-specific configs
                for subitem in item.iterdir():
                    if subitem.is_dir():
                        if subitem.name == 'default':
                            continue
                        compatibility['environments'].add(subitem.name)
                        
                        # Check for program directories
                        for prog_item in subitem.iterdir():
                            if prog_item.is_dir():
                                compatibility['programs'].add(prog_item.name)
        
        # Determine compatibility
        if compatibility['widgets']:
            compatibility['is_compatible'] = True
        else:
            compatibility['issues'].append("No widget directories found")
        
        return compatibility
    
    def list_available_repos(self, filter_tags: List[str] = None) -> List[Dict[str, str]]:
        """List available repositories, optionally filtered by tags"""
        repos = self.load_repo_list()
        
        if filter_tags:
            filtered_repos = []
            for repo in repos:
                if any(tag in repo.get('tags', []) for tag in filter_tags):
                    filtered_repos.append(repo)
            return filtered_repos
        
        return repos
    
    def install_from_git_repo(self, repo_name: str, widget_name: str = None, 
                            environment: Optional[Dict[str, str]] = None,
                            force_update: bool = False) -> bool:
        """Install configuration from a Git repository"""
        # Find the repository in our list
        repos = self.load_repo_list()
        repo_info = None
        for repo in repos:
            if repo['name'] == repo_name:
                repo_info = repo
                break
        
        if not repo_info:
            logger.error(f"Repository '{repo_name}' not found in compatible list")
            return False
        
        # Clone or update the repository
        if not self.clone_repo(repo_info, force_update):
            return False
        
        # Check compatibility
        repo_path = self.git_repos_dir / repo_name
        compatibility = self.check_repo_compatibility(repo_path)
        
        if not compatibility['is_compatible']:
            logger.error(f"Repository '{repo_name}' is not compatible: {compatibility['issues']}")
            return False
        
        # Install specific widget or all widgets
        if widget_name:
            if widget_name not in compatibility['widgets']:
                logger.error(f"Widget '{widget_name}' not found in repository '{repo_name}'")
                return False
            
            # Temporarily change repo path for installation
            original_repo_path = self.repo_path
            self.repo_path = repo_path
            success = self.install_widget(widget_name, environment)
            self.repo_path = original_repo_path
            return success
        else:
            # Install all widgets from the repository
            original_repo_path = self.repo_path
            self.repo_path = repo_path
            success = self.install_all_widgets(environment)
            self.repo_path = original_repo_path
            return success


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Dotfile Manager - Manage your dotfiles with environment detection")
    parser.add_argument('repo_path', help='Path to the dotfile repository')
    parser.add_argument('--config', '-c', help='Configuration file path (default: dotfile_config.json)')
    
    # Widget management
    parser.add_argument('--widget', '-w', help='Install specific widget only')
    parser.add_argument('--list', '-l', action='store_true', help='List available widgets')
    parser.add_argument('--info', '-i', help='Show information about a specific widget')
    
    # Git repository management
    parser.add_argument('--list-repos', action='store_true', help='List available Git repositories')
    parser.add_argument('--add-repo', nargs='+', 
                       help='Add a repository to the compatible list: URL [DESCRIPTION] [NAME] (NAME is optional, will be extracted from URL)')
    parser.add_argument('--no-fetch-metadata', action='store_true', help='Do not fetch metadata from repository files')
    parser.add_argument('--remove-repo', help='Remove a repository from the compatible list')
    parser.add_argument('--install-from-git', help='Install from a Git repository')
    parser.add_argument('--git-widget', help='Install specific widget from Git repository')
    parser.add_argument('--force-update', action='store_true', help='Force update Git repositories')
    parser.add_argument('--filter-tags', help='Filter repositories by tags (comma-separated)')
    parser.add_argument('--check-compatibility', help='Check compatibility of a Git repository')
    
    # Configuration management
    parser.add_argument('--pull-from-config', help='Pull existing configurations from ~/.config to repository structure')
    parser.add_argument('--output-dir', help='Custom output directory for pulled configurations (overrides repository structure)')
    parser.add_argument('--specific-programs', nargs='+', help='Specific programs to pull (e.g., alacritty kitty eww)')
    parser.add_argument('--use-config-fallback', action='store_true', help='Use ~/.config as fallback when installing')
    parser.add_argument('--check-program-compatibility', help='Check program compatibility for a specific widget')
    parser.add_argument('--list-compatible-programs', action='store_true', help='List all programs and their compatibility status')
    parser.add_argument('--update-compatibility', help='Update program compatibility file from URL or local path')
    parser.add_argument('--update-auto-config-rules', help='Update auto config rules file from URL or local path')
    
    # Installation options
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--no-backup', action='store_true', help='Do not backup existing files')
    parser.add_argument('--environment', '-e', help='Override environment detection (JSON format)')
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = DotfileManager(args.repo_path, args.config or "dotfile_config.json")
    
    # Override config with CLI arguments
    if args.dry_run:
        manager.config['dry_run'] = True
    if args.no_backup:
        manager.config['backup_existing'] = False
    
    # Parse environment override
    environment = None
    if args.environment:
        try:
            environment = json.loads(args.environment)
        except json.JSONDecodeError:
            logger.error("Invalid JSON format for environment override")
            return 1
    
    # Handle different commands
    if args.list:
        widgets = manager.list_widgets()
        print("Available widgets:")
        for widget in widgets:
            print(f"  - {widget}")
        return 0
    
    if args.info:
        manager.show_widget_info(args.info)
        return 0
    
    # Configuration management commands
    if args.pull_from_config:
        success = manager.pull_from_config(args.pull_from_config, args.environment, args.specific_programs, args.output_dir)
        return 0 if success else 1
    
    # Git repository management commands
    if args.list_repos:
        filter_tags = args.filter_tags.split(',') if args.filter_tags else None
        repos = manager.list_available_repos(filter_tags)
        print("Available Git repositories:")
        for repo in repos:
            tags_str = ', '.join(repo.get('tags', []))
            print(f"  - {repo['name']}: {repo.get('description', 'No description')}")
            print(f"    URL: {repo['url']}")
            if tags_str:
                print(f"    Tags: {tags_str}")
            print()
        return 0
    
    if args.add_repo:
        if len(args.add_repo) < 1:
            logger.error("URL is required for --add-repo")
            return 1
        
        url = args.add_repo[0]
        description = args.add_repo[1] if len(args.add_repo) > 1 else ""
        name = args.add_repo[2] if len(args.add_repo) > 2 else None
        tags = args.filter_tags.split(',') if args.filter_tags else []
        fetch_metadata = not args.no_fetch_metadata
        
        success = manager.add_repo(url, description, tags, name, fetch_metadata)
        if success:
            extracted_name = manager.extract_repo_name_from_url(url) if name is None else name
            print(f"Successfully added repository: {extracted_name}")
        return 0 if success else 1
    
    if args.remove_repo:
        success = manager.remove_repo(args.remove_repo)
        if success:
            print(f"Successfully removed repository: {args.remove_repo}")
        return 0 if success else 1
    
    if args.check_compatibility:
        repo_path = Path(args.check_compatibility)
        compatibility = manager.check_repo_compatibility(repo_path)
        print(f"Compatibility check for: {repo_path}")
        print(f"Compatible: {compatibility['is_compatible']}")
        if compatibility['widgets']:
            print(f"Widgets: {', '.join(compatibility['widgets'])}")
        if compatibility['environments']:
            print(f"Environments: {', '.join(compatibility['environments'])}")
        if compatibility['programs']:
            print(f"Programs: {', '.join(compatibility['programs'])}")
        if compatibility['issues']:
            print(f"Issues: {', '.join(compatibility['issues'])}")
        return 0
    
    if args.check_program_compatibility:
        widget_name = args.check_program_compatibility
        environment = environment or manager.detect_environment()
        
        config_path = manager.select_best_config(widget_name, environment)
        if not config_path:
            logger.error(f"No suitable configuration found for widget '{widget_name}'")
            return 1
        
        config_files = manager.get_config_files(config_path)
        if not config_files:
            logger.warning(f"No configuration files found in {config_path}")
            return 1
        
        print(f"Program compatibility check for widget: {widget_name}")
        print(f"Configuration path: {config_path}")
        print()
        
        compatibility_warnings = manager.check_program_compatibility(config_files, widget_name)
        
        if compatibility_warnings['single_config_warnings']:
            print("⚠️  COMPATIBILITY WARNINGS:")
            for warning in compatibility_warnings['single_config_warnings']:
                print(f"   {warning}")
            print()
        
        if compatibility_warnings['multiple_config_info']:
            print("ℹ️  COMPATIBILITY INFORMATION:")
            for info in compatibility_warnings['multiple_config_info']:
                print(f"   {info}")
            print()
        
        if not compatibility_warnings['single_config_warnings'] and not compatibility_warnings['multiple_config_info']:
            print("✅ No compatibility issues detected.")
        
        return 0
    
    if args.list_compatible_programs:
        print("Program Compatibility Status:")
        print("=" * 50)
        
        single_config = manager.program_compatibility.get('single_config_only', {})
        multiple_config = manager.program_compatibility.get('supports_multiple_configs', {})
        
        if single_config:
            print("\n⚠️  Single Configuration Programs:")
            for program, info in single_config.items():
                category = info.get('category', 'unknown')
                description = info.get('description', 'No description')
                print(f"  {program:<15} ({category:<12}) - {description}")
        
        if multiple_config:
            print("\n✅ Multiple Configuration Programs:")
            for program, info in multiple_config.items():
                category = info.get('category', 'unknown')
                description = info.get('description', 'No description')
                print(f"  {program:<15} ({category:<12}) - {description}")
        
        metadata = manager.program_compatibility.get('metadata', {})
        if metadata:
            print(f"\nVersion: {metadata.get('version', 'unknown')}")
            print(f"Last Updated: {metadata.get('last_updated', 'unknown')}")
        
        return 0
    
    if args.update_compatibility:
        # Update program compatibility file
        source = args.update_compatibility
        if source.startswith(('http://', 'https://')):
            # Download from URL
            try:
                import urllib.request
                urllib.request.urlretrieve(source, str(manager.program_compatibility_file))
                print(f"Successfully updated program compatibility file from {source}")
            except Exception as e:
                logger.error(f"Failed to download compatibility file: {e}")
                return 1
        else:
            # Copy from local path
            try:
                shutil.copy2(source, str(manager.program_compatibility_file))
                print(f"Successfully updated program compatibility file from {source}")
            except Exception as e:
                logger.error(f"Failed to copy compatibility file: {e}")
                return 1
        
        # Reload the compatibility settings
        manager.program_compatibility = manager._load_program_compatibility()
        return 0
    
    if args.update_auto_config_rules:
        # Update auto config rules file
        source = args.update_auto_config_rules
        if source.startswith(('http://', 'https://')):
            # Download from URL
            try:
                import urllib.request
                urllib.request.urlretrieve(source, str(manager.auto_config_rules_file))
                print(f"Successfully updated auto config rules file from {source}")
            except Exception as e:
                logger.error(f"Failed to download auto config rules file: {e}")
                return 1
        else:
            # Copy from local path
            try:
                shutil.copy2(source, str(manager.auto_config_rules_file))
                print(f"Successfully updated auto config rules file from {source}")
            except Exception as e:
                logger.error(f"Failed to copy auto config rules file: {e}")
                return 1
        
        # Reload the auto config rules
        manager.auto_config_rules = manager._load_auto_config_rules()
        return 0
    
    if args.install_from_git:
        if args.git_widget:
            success = manager.install_from_git_repo(args.install_from_git, args.git_widget, 
                                                  environment, args.force_update)
        else:
            success = manager.install_from_git_repo(args.install_from_git, None, 
                                                  environment, args.force_update)
        return 0 if success else 1
    
    # Regular widget installation
    if args.widget:
        success = manager.install_widget(args.widget, environment, args.use_config_fallback)
    else:
        success = manager.install_all_widgets(environment)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
