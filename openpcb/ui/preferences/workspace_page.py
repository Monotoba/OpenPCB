"""Workspace settings page for preferences dialog."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from openpcb.config import config_manager


class WorkspaceSettingsPage(QWidget):
    """Workspace settings configuration page."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize workspace settings page."""
        super().__init__(parent)

        self._setup_ui()
        self.load_settings()

    def _setup_ui(self) -> None:
        """Setup page UI."""
        layout = QVBoxLayout(self)

        # Profile group
        profile_group = QGroupBox("Profile")
        profile_layout = QFormLayout(profile_group)

        self.active_profile_edit = QLineEdit()
        profile_layout.addRow("Active Profile:", self.active_profile_edit)

        layout.addWidget(profile_group)

        # Recent files group
        recent_group = QGroupBox("Recent Files")
        recent_layout = QFormLayout(recent_group)

        self.last_project_label = QLabel()
        self.last_project_label.setWordWrap(True)
        self.last_project_label.setStyleSheet("QLabel { color: #888; }")

        recent_layout.addRow("Last Project Directory:", self.last_project_label)

        layout.addWidget(recent_group)

        # Panel visibility group
        panels_group = QGroupBox("Panel Visibility")
        panels_layout = QFormLayout(panels_group)

        self.show_layer_panel_check = QCheckBox()
        self.show_properties_panel_check = QCheckBox()
        self.show_tool_panel_check = QCheckBox()

        panels_layout.addRow("Show Layer Panel:", self.show_layer_panel_check)
        panels_layout.addRow("Show Properties Panel:", self.show_properties_panel_check)
        panels_layout.addRow("Show Tool Panel:", self.show_tool_panel_check)

        layout.addWidget(panels_group)

        layout.addStretch()

    def load_settings(self) -> None:
        """Load current settings into UI."""
        config = config_manager.config.workspace

        self.active_profile_edit.setText(config.active_profile)

        last_dir = config.last_project_directory or "None"
        self.last_project_label.setText(last_dir)

        self.show_layer_panel_check.setChecked(config.show_layer_panel)
        self.show_properties_panel_check.setChecked(config.show_properties_panel)
        self.show_tool_panel_check.setChecked(config.show_tool_panel)

    def apply_settings(self) -> None:
        """Apply settings from UI."""
        config_manager.update_workspace(
            active_profile=self.active_profile_edit.text(),
            show_layer_panel=self.show_layer_panel_check.isChecked(),
            show_properties_panel=self.show_properties_panel_check.isChecked(),
            show_tool_panel=self.show_tool_panel_check.isChecked(),
        )
