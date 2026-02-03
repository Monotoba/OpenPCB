"""
Configuration data models for OpenPCB.

Uses Pydantic for validation, serialization, and type safety.
All settings are immutable by default (frozen=True) to prevent accidental modification.
"""

from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator


class Units(str, Enum):
    """Measurement units for display."""

    MILLIMETERS = "mm"
    INCHES = "in"


class ColorScheme(str, Enum):
    """Application color scheme."""

    SYSTEM = "system"  # Follow system theme
    LIGHT = "light"
    DARK = "dark"


class HiDPIScaleMode(str, Enum):
    """HiDPI scaling behavior."""

    AUTO = "auto"  # Qt automatic scaling
    SYSTEM = "system"  # Use system DPI
    CUSTOM = "custom"  # User-defined scale factor


# Window geometry storage
class WindowGeometry(BaseModel):
    """Window position and size."""

    x: int = 100
    y: int = 100
    width: int = 1280
    height: int = 800
    maximized: bool = False

    model_config = {"frozen": True}


# Display settings
class DisplaySettings(BaseModel):
    """Viewer and display configuration."""

    # Grid settings
    grid_visible: bool = True
    grid_size_mm: Annotated[float, Field(gt=0.0, le=100.0)] = 1.0
    grid_subdivisions: Annotated[int, Field(ge=1, le=10)] = 10
    snap_to_grid: bool = True

    # Zoom and pan
    zoom_default: Annotated[float, Field(gt=0.1, le=10.0)] = 1.0
    pan_speed: Annotated[float, Field(gt=0.1, le=5.0)] = 1.0
    zoom_speed: Annotated[float, Field(gt=0.1, le=5.0)] = 1.2

    # Units
    units: Units = Units.MILLIMETERS
    decimal_places: Annotated[int, Field(ge=0, le=6)] = 3

    # Colors (hex format)
    background_color: str = "#2b2b2b"
    grid_color: str = "#3c3c3c"
    cursor_color: str = "#ff9900"
    selection_color: str = "#00aaff"

    # Visual settings
    antialiasing: bool = True
    show_rulers: bool = True
    show_origin: bool = True

    # Color scheme
    color_scheme: ColorScheme = ColorScheme.SYSTEM

    model_config = {"frozen": True}

    @field_validator("background_color", "grid_color", "cursor_color", "selection_color")
    @classmethod
    def validate_hex_color(cls, v: str) -> str:
        """Validate hex color format."""
        if not v.startswith("#") or len(v) not in (4, 7):
            raise ValueError(f"Invalid hex color: {v}")
        try:
            int(v[1:], 16)
        except ValueError as e:
            raise ValueError(f"Invalid hex color: {v}") from e
        return v.lower()


# HiDPI settings
class HiDPISettings(BaseModel):
    """High-DPI display configuration."""

    scale_mode: HiDPIScaleMode = HiDPIScaleMode.AUTO
    custom_scale_factor: Annotated[float, Field(ge=0.5, le=4.0)] = 1.0

    # Font scaling
    font_scale_factor: Annotated[float, Field(ge=0.5, le=3.0)] = 1.0

    # Icon sizes (in logical pixels)
    toolbar_icon_size: Annotated[int, Field(ge=16, le=128)] = 24
    menu_icon_size: Annotated[int, Field(ge=12, le=64)] = 16

    # Qt-specific flags
    enable_high_dpi_scaling: bool = True
    use_high_dpi_pixmaps: bool = True
    round_scale_factor: bool = False  # False for fractional scaling

    model_config = {"frozen": True}


# Application settings
class ApplicationSettings(BaseModel):
    """General application configuration."""

    # Window state
    window_geometry: WindowGeometry = Field(default_factory=WindowGeometry)

    # Recent files
    recent_files: list[str] = Field(default_factory=list, max_length=10)
    recent_projects_max: Annotated[int, Field(ge=5, le=50)] = 10

    # Autosave
    autosave_enabled: bool = True
    autosave_interval_seconds: Annotated[int, Field(ge=30, le=3600)] = 300

    # Startup behavior
    restore_last_session: bool = True
    show_splash_screen: bool = True
    check_updates_on_startup: bool = True

    model_config = {"frozen": True}


# Workspace settings
class WorkspaceSettings(BaseModel):
    """Workspace and tool configuration."""

    active_profile: str = "default"
    last_used_tool: str | None = None
    last_project_directory: str | None = None

    # Dock layout (serialized Qt state)
    dock_layout: bytes | None = None

    # Tool panel visibility
    show_layer_panel: bool = True
    show_properties_panel: bool = True
    show_tool_panel: bool = True

    model_config = {"frozen": True}


# Root configuration
class OpenPCBConfig(BaseModel):
    """Root configuration for OpenPCB application."""

    # Config schema version for migration
    schema_version: Literal[1] = 1

    # Setting groups
    application: ApplicationSettings = Field(default_factory=ApplicationSettings)
    display: DisplaySettings = Field(default_factory=DisplaySettings)
    hidpi: HiDPISettings = Field(default_factory=HiDPISettings)
    workspace: WorkspaceSettings = Field(default_factory=WorkspaceSettings)

    model_config = {"frozen": True}

    def model_dump_json_safe(self) -> dict:
        """Dump model to JSON-safe dict (convert bytes to base64)."""
        import base64

        data = self.model_dump()

        # Convert bytes fields to base64 strings
        if data["workspace"]["dock_layout"] is not None:
            data["workspace"]["dock_layout"] = base64.b64encode(
                data["workspace"]["dock_layout"]
            ).decode("ascii")

        return data

    @classmethod
    def model_validate_json_safe(cls, data: dict) -> OpenPCBConfig:
        """Load model from JSON-safe dict (convert base64 to bytes)."""
        import base64

        # Convert base64 strings back to bytes
        if data.get("workspace", {}).get("dock_layout") is not None:
            data["workspace"]["dock_layout"] = base64.b64decode(
                data["workspace"]["dock_layout"]
            )

        return cls.model_validate(data)
