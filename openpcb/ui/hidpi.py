"""
HiDPI display support for OpenPCB.

Configures Qt for optimal rendering on high-resolution displays.
Must be called before QApplication instantiation.

## Known Issues and Solutions

### Menu Dropdown Misalignment on GNOME with HiDPI (Fixed)

**Issue**: On GNOME desktop environments with HiDPI scaling (e.g., QT_SCALE_FACTOR=2.0),
menu dropdowns appear at incorrect positions. For example, clicking "File" in the menu
bar would cause the dropdown to appear under the "View" menu instead.

**Root Cause**: Double scaling conflict. When QT_SCALE_FACTOR is set externally
(by desktop environment or user), Qt 6's automatic scaling can multiply this factor
rather than using it directly. This causes geometry calculations (especially for menus)
to be incorrect.

**Solution**: When an external QT_SCALE_FACTOR is detected in "auto" mode, we explicitly
disable Qt's automatic scaling by setting:
- QT_AUTO_SCREEN_SCALE_FACTOR=0
- QT_ENABLE_HIGHDPI_SCALING=0

This prevents double scaling while preserving the user's desired scale factor.

**References**:
- Qt 6 HiDPI Documentation: https://doc.qt.io/qt-6/highdpi.html
- Qt Bug QTBUG-52606: Menu positioning issues with HiDPI
- ArchWiki HiDPI Guide: https://wiki.archlinux.org/title/HiDPI

**Additional Fix**: The application also sets Qt.AA_DontUseNativeMenuBar to prevent
GNOME's global menu system from interfering with Qt menu bar rendering.
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

    # Check if QT_SCALE_FACTOR is set externally
    external_scale = os.environ.get("QT_SCALE_FACTOR")

    if external_scale and settings.scale_mode == "auto":
        # CRITICAL FIX for menu positioning on HiDPI displays:
        # Prevent double scaling when QT_SCALE_FACTOR is manually set by the desktop
        # environment (e.g., GNOME with 2x scaling). Without these settings, Qt 6
        # multiplies the scale factor causing incorrect geometry calculations,
        # especially for menu dropdowns which appear offset from their menu bar items.
        # See: https://doc.qt.io/qt-6/highdpi.html
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        logger.info(f"External QT_SCALE_FACTOR={external_scale} detected - disabled automatic scaling")
    elif settings.scale_mode == "custom":
        # Custom scale factor
        os.environ["QT_SCALE_FACTOR"] = str(settings.custom_scale_factor)
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        logger.info(f"Set custom scale factor: {settings.custom_scale_factor}")
    else:
        # Auto/system mode - let Qt handle scaling automatically
        os.environ.pop("QT_SCALE_FACTOR", None)
        if settings.enable_high_dpi_scaling:
            os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
        if settings.use_high_dpi_pixmaps:
            os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        logger.debug("Using Qt automatic scaling")

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
