"""
Default configuration presets for OpenPCB.

Provides common configurations for different workflows and display setups.
"""

from .models import ColorScheme, DisplaySettings, HiDPIScaleMode, HiDPISettings, OpenPCBConfig, Units

# Display presets
DISPLAY_DARK_THEME = DisplaySettings(
    background_color="#1e1e1e",
    grid_color="#2d2d2d",
    cursor_color="#ff9900",
    selection_color="#00aaff",
    color_scheme=ColorScheme.DARK,
)

DISPLAY_LIGHT_THEME = DisplaySettings(
    background_color="#ffffff",
    grid_color="#e0e0e0",
    cursor_color="#ff6600",
    selection_color="#0080ff",
    color_scheme=ColorScheme.LIGHT,
)

DISPLAY_HIGH_CONTRAST = DisplaySettings(
    background_color="#000000",
    grid_color="#404040",
    cursor_color="#ffff00",
    selection_color="#00ffff",
    antialiasing=False,  # Sharper on some displays
    color_scheme=ColorScheme.DARK,
)

# HiDPI presets
HIDPI_AUTO = HiDPISettings(
    scale_mode=HiDPIScaleMode.AUTO,
    enable_high_dpi_scaling=True,
    use_high_dpi_pixmaps=True,
)

HIDPI_4K = HiDPISettings(
    scale_mode=HiDPIScaleMode.CUSTOM,
    custom_scale_factor=2.0,
    font_scale_factor=1.5,
    toolbar_icon_size=32,
    menu_icon_size=20,
)

HIDPI_DISABLED = HiDPISettings(
    scale_mode=HiDPIScaleMode.SYSTEM,
    enable_high_dpi_scaling=False,
    use_high_dpi_pixmaps=False,
    custom_scale_factor=1.0,
)

# Units presets
UNITS_METRIC = {"units": Units.MILLIMETERS, "decimal_places": 3}
UNITS_IMPERIAL = {"units": Units.INCHES, "decimal_places": 4}


def get_preset(name: str) -> OpenPCBConfig | None:
    """
    Get a preset configuration by name.

    Available presets:
    - "default": Standard dark theme, auto HiDPI
    - "light": Light theme, auto HiDPI
    - "high-contrast": High contrast theme, auto HiDPI
    - "4k": Dark theme, 4K display optimized
    - "no-scaling": Dark theme, HiDPI disabled
    """
    presets = {
        "default": OpenPCBConfig(),
        "light": OpenPCBConfig(display=DISPLAY_LIGHT_THEME),
        "high-contrast": OpenPCBConfig(display=DISPLAY_HIGH_CONTRAST),
        "4k": OpenPCBConfig(display=DISPLAY_DARK_THEME, hidpi=HIDPI_4K),
        "no-scaling": OpenPCBConfig(display=DISPLAY_DARK_THEME, hidpi=HIDPI_DISABLED),
    }

    return presets.get(name)
