"""
HiDPI display support for OpenPCB.

Configures Qt for optimal rendering on high-resolution displays.
Must be called before QApplication instantiation.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openpcb.config.models import HiDPISettings

logger = logging.getLogger(__name__)


def configure_hidpi(settings: HiDPISettings | None = None) -> None:
    """
    Configure Qt for HiDPI displays.

    Must be called before creating QApplication instance.

    Args:
        settings: HiDPI settings to apply. If None, uses config_manager.
    """
    if settings is None:
        from openpcb.config import config_manager

        settings = config_manager.config.hidpi

    logger.info(f"Configuring HiDPI: mode={settings.scale_mode}")

    # Enable high DPI scaling
    if settings.enable_high_dpi_scaling:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
        logger.debug("Enabled Qt high DPI scaling")
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        logger.debug("Disabled Qt high DPI scaling")

    # High DPI pixmaps
    if settings.use_high_dpi_pixmaps:
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        logger.debug("Enabled high DPI pixmaps")

    # Scale factor rounding
    if settings.round_scale_factor:
        os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "Round"
    else:
        os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"

    # Custom scale factor
    if settings.scale_mode == "custom":
        os.environ["QT_SCALE_FACTOR"] = str(settings.custom_scale_factor)
        logger.info(f"Set custom scale factor: {settings.custom_scale_factor}")
    elif settings.scale_mode == "system":
        # Let system handle scaling
        os.environ.pop("QT_SCALE_FACTOR", None)
        logger.debug("Using system DPI scaling")

    # Platform-specific tweaks
    if sys.platform == "win32":
        # Windows: Enable per-monitor DPI awareness
        try:
            import ctypes

            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
            logger.debug("Enabled per-monitor DPI awareness (Windows)")
        except Exception as e:
            logger.warning(f"Could not set DPI awareness: {e}")

    elif sys.platform == "darwin":
        # macOS: Retina display support (usually automatic)
        logger.debug("macOS Retina support enabled")


def apply_hidpi_stylesheet(app, settings: HiDPISettings | None = None) -> None:
    """
    Apply HiDPI-aware stylesheet to application.

    Adjusts font sizes, icon sizes, and spacing based on settings.

    Args:
        app: QApplication instance
        settings: HiDPI settings to apply
    """
    if settings is None:
        from openpcb.config import config_manager

        settings = config_manager.config.hidpi

    base_font_size = int(10 * settings.font_scale_factor)

    stylesheet = f"""
    QMainWindow {{
        font-size: {base_font_size}pt;
    }}

    QToolBar {{
        spacing: {int(4 * settings.font_scale_factor)}px;
    }}

    QDockWidget {{
        font-size: {base_font_size}pt;
    }}

    QStatusBar {{
        font-size: {int(9 * settings.font_scale_factor)}pt;
    }}
    """

    app.setStyleSheet(stylesheet)
    logger.debug("Applied HiDPI stylesheet")


def get_logical_dpi() -> tuple[float, float]:
    """
    Get logical DPI of primary screen.

    Returns:
        Tuple of (dpi_x, dpi_y)
    """
    from PySide6.QtWidgets import QApplication

    screen = QApplication.primaryScreen()
    if screen:
        dpi = screen.logicalDotsPerInch()
        return (dpi, dpi)

    return (96.0, 96.0)  # Standard DPI fallback


def get_device_pixel_ratio() -> float:
    """
    Get device pixel ratio of primary screen.

    Returns:
        Device pixel ratio (e.g., 2.0 for Retina displays)
    """
    from PySide6.QtWidgets import QApplication

    screen = QApplication.primaryScreen()
    if screen:
        return screen.devicePixelRatio()

    return 1.0
