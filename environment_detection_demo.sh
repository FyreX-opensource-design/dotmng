#!/bin/bash
# Environment Detection Demo Script
# This script demonstrates the enhanced environment detection system

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="${SCRIPT_DIR}/<example-git>"
CONFIG_FILE="${SCRIPT_DIR}/dotfile_config.json"

echo "=========================================="
echo "  Environment Detection Demo"
echo "=========================================="
echo

echo "This demo shows how the dotfile manager detects your environment"
echo "using environment variables as the primary method, with process"
echo "detection as a fallback."
echo

echo "1. Current Environment Variables:"
echo "--------------------------------"
echo "Window Manager Detection:"
echo "  DESKTOP_SESSION: ${DESKTOP_SESSION:-'Not set'}"
echo "  XDG_CURRENT_DESKTOP: ${XDG_CURRENT_DESKTOP:-'Not set'}"
echo "  HYPRLAND_INSTANCE_SIGNATURE: ${HYPRLAND_INSTANCE_SIGNATURE:-'Not set'}"
echo "  LABWC_SOCKET: ${LABWC_SOCKET:-'Not set'}"
echo "  SWAYSOCK: ${SWAYSOCK:-'Not set'}"
echo "  I3SOCK: ${I3SOCK:-'Not set'}"
echo

echo "Compositor Detection:"
echo "  WAYLAND_DISPLAY: ${WAYLAND_DISPLAY:-'Not set'}"
echo "  XDG_SESSION_TYPE: ${XDG_SESSION_TYPE:-'Not set'}"
echo "  PICOM_CONFIG: ${PICOM_CONFIG:-'Not set'}"
echo

echo "Shell Detection:"
echo "  SHELL: ${SHELL:-'Not set'}"
echo

echo "Terminal Detection:"
echo "  TERM: ${TERM:-'Not set'}"
echo

echo "2. Detected Environment:"
echo "----------------------"
python3 "${SCRIPT_DIR}/dotfile_manager.py" "${REPO_PATH}" --config "${CONFIG_FILE}" --check-program-compatibility "<example-widget-1>" 2>&1 | grep "Detected environment" || echo "No environment detection output found"
echo

echo "3. Environment Detection Priority:"
echo "--------------------------------"
echo "Window Manager Detection Order:"
echo "  1. Specific environment variables (HYPRLAND_INSTANCE_SIGNATURE, LABWC_SOCKET, etc.)"
echo "  2. DESKTOP_SESSION environment variable"
echo "  3. XDG_CURRENT_DESKTOP environment variable"
echo "  4. Process detection (ps -e) as fallback"
echo

echo "Compositor Detection Order:"
echo "  1. WAYLAND_DISPLAY environment variable"
echo "  2. PICOM_CONFIG environment variable"
echo "  3. XDG_SESSION_TYPE environment variable"
echo "  4. Process detection (ps -e) as fallback"
echo

echo "4. Benefits of Environment Variable Detection:"
echo "--------------------------------------------"
echo "✓ More reliable than process detection"
echo "✓ Faster (no subprocess calls needed)"
echo "✓ Works even when processes aren't running"
echo "✓ Standard environment variables used by most systems"
echo "✓ Handles Wayland vs X11 detection properly"
echo "✓ Supports both session managers and window managers"
echo

echo "5. Supported Environment Variables:"
echo "---------------------------------"
echo "Window Managers:"
echo "  - HYPRLAND_INSTANCE_SIGNATURE (Hyprland)"
echo "  - LABWC_SOCKET (LabWC)"
echo "  - SWAYSOCK (Sway)"
echo "  - I3SOCK (i3)"
echo "  - DESKTOP_SESSION (Session manager)"
echo "  - XDG_CURRENT_DESKTOP (Desktop environment)"
echo

echo "Compositors:"
echo "  - WAYLAND_DISPLAY (Wayland compositor)"
echo "  - PICOM_CONFIG (Picom configuration)"
echo "  - XDG_SESSION_TYPE (Session type)"
echo

echo "6. Example Environment Variable Values:"
echo "-------------------------------------"
echo "Hyprland:"
echo "  DESKTOP_SESSION=hyprland"
echo "  XDG_CURRENT_DESKTOP=Hyprland"
echo "  HYPRLAND_INSTANCE_SIGNATURE=hyprland-..."
echo

echo "LabWC:"
echo "  DESKTOP_SESSION=labwc"
echo "  XDG_CURRENT_DESKTOP=labwc:wlroots"
echo "  WAYLAND_DISPLAY=wayland-0"
echo

echo "Sway:"
echo "  DESKTOP_SESSION=sway"
echo "  XDG_CURRENT_DESKTOP=Sway"
echo "  SWAYSOCK=/run/user/1000/sway-ipc.1000.1234.sock"
echo

echo "i3:"
echo "  DESKTOP_SESSION=i3"
echo "  XDG_CURRENT_DESKTOP=i3"
echo "  I3SOCK=/run/user/1000/i3/ipc-socket.1234"
echo

echo "=========================================="
echo "Environment Detection Features:"
echo "✓ Environment variable priority detection"
echo "✓ Process detection fallback"
echo "✓ Wayland vs X11 detection"
echo "✓ Multiple window manager support"
echo "✓ Compositor detection"
echo "✓ Shell and terminal detection"
echo "✓ Fast and reliable detection"
echo "=========================================="
