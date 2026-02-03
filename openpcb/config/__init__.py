"""
Configuration management for OpenPCB.

Usage:
    from openpcb.config import config_manager

    # Access settings
    units = config_manager.config.display.units

    # Update settings
    config_manager.update_display(grid_visible=True)

    # Get platform directories
    config_dir = config_manager.config_dir
"""

from .defaults import get_preset
from .manager import ConfigManager, config_manager
from .models import (
    ApplicationSettings,
    ColorScheme,
    DisplaySettings,
    HiDPIScaleMode,
    HiDPISettings,
    OpenPCBConfig,
    Units,
    WindowGeometry,
    WorkspaceSettings,
)

__all__ = [
    # Manager
    "ConfigManager",
    "config_manager",
    # Models
    "OpenPCBConfig",
    "ApplicationSettings",
    "DisplaySettings",
    "HiDPISettings",
    "WindowGeometry",
    "WorkspaceSettings",
    # Enums
    "Units",
    "ColorScheme",
    "HiDPIScaleMode",
    # Utilities
    "get_preset",
]
