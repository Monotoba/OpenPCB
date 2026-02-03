"""
OpenPCB application entry point.

Initializes configuration, HiDPI support, and GUI.
"""

from __future__ import annotations

import logging
import sys


def setup_logging() -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main_gui() -> int:
    """
    Launch OpenPCB GUI application.

    Returns:
        Exit code (0 for success)
    """
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Import Qt first to set attributes
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import QApplication

        # Set Qt attributes BEFORE creating QApplication
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        # CRITICAL FIX for GNOME menu positioning:
        # Disable native menu bar to prevent GNOME's global menu system from
        # interfering with Qt menu rendering. Without this, menu dropdowns can
        # appear at incorrect positions, especially on HiDPI displays.
        # This forces Qt to render menus in-window rather than using the desktop's
        # native menu system.
        QApplication.setAttribute(Qt.AA_DontUseNativeMenuBar, True)

        # Configure HiDPI environment variables
        from openpcb.ui.hidpi import configure_hidpi

        configure_hidpi()

        from openpcb.ui.mainwindow import MainWindow

        logger.info("Starting OpenPCB GUI...")

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("OpenPCB")
        app.setOrganizationName("OpenPCB")
        app.setOrganizationDomain("openpcb.org")

        # Apply HiDPI stylesheet
        from openpcb.ui.hidpi import apply_hidpi_stylesheet

        apply_hidpi_stylesheet(app)

        # Create and show main window
        window = MainWindow()
        window.show()

        logger.info("OpenPCB GUI started successfully")

        return app.exec()

    except Exception as e:
        logger.exception(f"Failed to start OpenPCB GUI: {e}")
        return 1


def main() -> None:
    """Main entry point - delegates to CLI or GUI."""
    if len(sys.argv) > 1:
        # Command-line arguments provided - use CLI
        from openpcb.cli import main as cli_main

        cli_main()
    else:
        # No arguments - launch GUI
        sys.exit(main_gui())


if __name__ == "__main__":
    main()
