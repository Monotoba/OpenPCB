"""
Preferences dialog for OpenPCB.

Multi-page dialog for configuring application settings.
"""

from __future__ import annotations

import logging

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QListWidget,
    QMessageBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from openpcb.config import config_manager

from .display_page import DisplaySettingsPage
from .hidpi_page import HiDPISettingsPage
from .workspace_page import WorkspaceSettingsPage

logger = logging.getLogger(__name__)


class PreferencesDialog(QDialog):
    """
    Preferences dialog with multiple pages.

    Pages:
    - Display: Grid, colors, units, zoom settings
    - HiDPI: High-resolution display settings
    - Workspace: Active profile, tool settings
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize preferences dialog."""
        super().__init__(parent)

        self.setWindowTitle("Preferences")
        self.setModal(True)
        self.setMinimumSize(800, 600)

        self._setup_ui()

        logger.info("Preferences dialog opened")

    def _setup_ui(self) -> None:
        """Setup dialog UI."""
        layout = QVBoxLayout(self)

        # Main area: list + pages
        main_layout = QHBoxLayout()

        # Category list (left)
        self.category_list = QListWidget()
        self.category_list.addItem("Display")
        self.category_list.addItem("HiDPI")
        self.category_list.addItem("Workspace")
        self.category_list.setMaximumWidth(200)
        self.category_list.setCurrentRow(0)
        self.category_list.currentRowChanged.connect(self._on_category_changed)

        # Pages stack (right)
        self.pages = QStackedWidget()

        # Create pages
        self.display_page = DisplaySettingsPage()
        self.hidpi_page = HiDPISettingsPage()
        self.workspace_page = WorkspaceSettingsPage()

        self.pages.addWidget(self.display_page)
        self.pages.addWidget(self.hidpi_page)
        self.pages.addWidget(self.workspace_page)

        main_layout.addWidget(self.category_list)
        main_layout.addWidget(self.pages, 1)

        layout.addLayout(main_layout, 1)

        # Button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply
            | QDialogButtonBox.StandardButton.RestoreDefaults
        )
        button_box.accepted.connect(self._on_ok)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self._on_apply)
        button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(
            self._on_restore_defaults
        )

        layout.addWidget(button_box)

    def _on_category_changed(self, index: int) -> None:
        """Handle category selection change."""
        self.pages.setCurrentIndex(index)

    def _on_ok(self) -> None:
        """Handle OK button."""
        self._apply_changes()
        self.accept()

    def _on_apply(self) -> None:
        """Handle Apply button."""
        self._apply_changes()

    def _on_restore_defaults(self) -> None:
        """Handle Restore Defaults button."""
        logger.info("Restoring default settings")

        reply = QMessageBox.question(
            self,
            "Restore Defaults",
            "Are you sure you want to restore all settings to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            config_manager.reset_to_defaults()

            # Reload pages
            self.display_page.load_settings()
            self.hidpi_page.load_settings()
            self.workspace_page.load_settings()

    def _apply_changes(self) -> None:
        """Apply changes from all pages."""
        logger.info("Applying preferences changes")

        self.display_page.apply_settings()
        self.hidpi_page.apply_settings()
        self.workspace_page.apply_settings()

        logger.info("Preferences saved")
