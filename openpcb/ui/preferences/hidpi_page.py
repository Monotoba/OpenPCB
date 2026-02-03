"""HiDPI settings page for preferences dialog."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from openpcb.config import HiDPIScaleMode, config_manager


class HiDPISettingsPage(QWidget):
    """HiDPI settings configuration page."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize HiDPI settings page."""
        super().__init__(parent)

        self._setup_ui()
        self.load_settings()

    def _setup_ui(self) -> None:
        """Setup page UI."""
        layout = QVBoxLayout(self)

        # Scaling group
        scaling_group = QGroupBox("Display Scaling")
        scaling_layout = QFormLayout(scaling_group)

        self.scale_mode_combo = QComboBox()
        self.scale_mode_combo.addItems(["Auto", "System", "Custom"])
        self.scale_mode_combo.currentIndexChanged.connect(self._on_scale_mode_changed)

        self.custom_scale_spin = QDoubleSpinBox()
        self.custom_scale_spin.setRange(0.5, 4.0)
        self.custom_scale_spin.setSingleStep(0.1)
        self.custom_scale_spin.setDecimals(2)

        scaling_layout.addRow("Scale Mode:", self.scale_mode_combo)
        scaling_layout.addRow("Custom Scale Factor:", self.custom_scale_spin)

        layout.addWidget(scaling_group)

        # Font scaling group
        font_group = QGroupBox("Font Scaling")
        font_layout = QFormLayout(font_group)

        self.font_scale_spin = QDoubleSpinBox()
        self.font_scale_spin.setRange(0.5, 3.0)
        self.font_scale_spin.setSingleStep(0.1)
        self.font_scale_spin.setDecimals(2)

        font_layout.addRow("Font Scale Factor:", self.font_scale_spin)

        layout.addWidget(font_group)

        # Icon sizes group
        icon_group = QGroupBox("Icon Sizes")
        icon_layout = QFormLayout(icon_group)

        self.toolbar_icon_spin = QSpinBox()
        self.toolbar_icon_spin.setRange(16, 128)
        self.toolbar_icon_spin.setSuffix(" px")

        self.menu_icon_spin = QSpinBox()
        self.menu_icon_spin.setRange(12, 64)
        self.menu_icon_spin.setSuffix(" px")

        icon_layout.addRow("Toolbar Icon Size:", self.toolbar_icon_spin)
        icon_layout.addRow("Menu Icon Size:", self.menu_icon_spin)

        layout.addWidget(icon_group)

        # Advanced options group
        advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QFormLayout(advanced_group)

        self.enable_scaling_check = QCheckBox()
        self.use_pixmaps_check = QCheckBox()
        self.round_scale_check = QCheckBox()

        advanced_layout.addRow("Enable High DPI Scaling:", self.enable_scaling_check)
        advanced_layout.addRow("Use High DPI Pixmaps:", self.use_pixmaps_check)
        advanced_layout.addRow("Round Scale Factor:", self.round_scale_check)

        layout.addWidget(advanced_group)

        layout.addStretch()

    def _on_scale_mode_changed(self, index: int) -> None:
        """Handle scale mode change."""
        # Enable custom scale only when mode is Custom
        self.custom_scale_spin.setEnabled(index == 2)

    def load_settings(self) -> None:
        """Load current settings into UI."""
        config = config_manager.config.hidpi

        # Scale mode
        mode_map = {"auto": 0, "system": 1, "custom": 2}
        self.scale_mode_combo.setCurrentIndex(mode_map.get(config.scale_mode.value, 0))

        self.custom_scale_spin.setValue(config.custom_scale_factor)
        self._on_scale_mode_changed(self.scale_mode_combo.currentIndex())

        # Font scaling
        self.font_scale_spin.setValue(config.font_scale_factor)

        # Icon sizes
        self.toolbar_icon_spin.setValue(config.toolbar_icon_size)
        self.menu_icon_spin.setValue(config.menu_icon_size)

        # Advanced options
        self.enable_scaling_check.setChecked(config.enable_high_dpi_scaling)
        self.use_pixmaps_check.setChecked(config.use_high_dpi_pixmaps)
        self.round_scale_check.setChecked(config.round_scale_factor)

    def apply_settings(self) -> None:
        """Apply settings from UI."""
        mode_values = [HiDPIScaleMode.AUTO, HiDPIScaleMode.SYSTEM, HiDPIScaleMode.CUSTOM]
        scale_mode = mode_values[self.scale_mode_combo.currentIndex()]

        config_manager.update_hidpi(
            scale_mode=scale_mode,
            custom_scale_factor=self.custom_scale_spin.value(),
            font_scale_factor=self.font_scale_spin.value(),
            toolbar_icon_size=self.toolbar_icon_spin.value(),
            menu_icon_size=self.menu_icon_spin.value(),
            enable_high_dpi_scaling=self.enable_scaling_check.isChecked(),
            use_high_dpi_pixmaps=self.use_pixmaps_check.isChecked(),
            round_scale_factor=self.round_scale_check.isChecked(),
        )
