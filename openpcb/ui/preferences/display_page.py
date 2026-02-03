"""Display settings page for preferences dialog."""

from __future__ import annotations

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from openpcb.config import ColorScheme, Units, config_manager


class DisplaySettingsPage(QWidget):
    """Display settings configuration page."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize display settings page."""
        super().__init__(parent)

        self._setup_ui()
        self.load_settings()

    def _setup_ui(self) -> None:
        """Setup page UI."""
        layout = QVBoxLayout(self)

        # Grid settings group
        grid_group = QGroupBox("Grid")
        grid_layout = QFormLayout(grid_group)

        self.grid_visible_check = QCheckBox()
        self.grid_size_spin = QDoubleSpinBox()
        self.grid_size_spin.setRange(0.1, 100.0)
        self.grid_size_spin.setSuffix(" mm")
        self.grid_size_spin.setDecimals(2)
        self.snap_to_grid_check = QCheckBox()

        grid_layout.addRow("Visible:", self.grid_visible_check)
        grid_layout.addRow("Size:", self.grid_size_spin)
        grid_layout.addRow("Snap to Grid:", self.snap_to_grid_check)

        layout.addWidget(grid_group)

        # Units group
        units_group = QGroupBox("Units")
        units_layout = QFormLayout(units_group)

        self.units_combo = QComboBox()
        self.units_combo.addItems(["Millimeters", "Inches"])

        self.decimal_places_spin = QSpinBox()
        self.decimal_places_spin.setRange(0, 6)

        units_layout.addRow("Display Units:", self.units_combo)
        units_layout.addRow("Decimal Places:", self.decimal_places_spin)

        layout.addWidget(units_group)

        # Colors group
        colors_group = QGroupBox("Colors")
        colors_layout = QFormLayout(colors_group)

        self.bg_color_btn = QPushButton()
        self.bg_color_btn.clicked.connect(lambda: self._choose_color("background"))

        self.grid_color_btn = QPushButton()
        self.grid_color_btn.clicked.connect(lambda: self._choose_color("grid"))

        self.cursor_color_btn = QPushButton()
        self.cursor_color_btn.clicked.connect(lambda: self._choose_color("cursor"))

        self.selection_color_btn = QPushButton()
        self.selection_color_btn.clicked.connect(lambda: self._choose_color("selection"))

        colors_layout.addRow("Background:", self.bg_color_btn)
        colors_layout.addRow("Grid:", self.grid_color_btn)
        colors_layout.addRow("Cursor:", self.cursor_color_btn)
        colors_layout.addRow("Selection:", self.selection_color_btn)

        layout.addWidget(colors_group)

        # Visual settings group
        visual_group = QGroupBox("Visual")
        visual_layout = QFormLayout(visual_group)

        self.antialiasing_check = QCheckBox()
        self.show_rulers_check = QCheckBox()
        self.show_origin_check = QCheckBox()

        visual_layout.addRow("Antialiasing:", self.antialiasing_check)
        visual_layout.addRow("Show Rulers:", self.show_rulers_check)
        visual_layout.addRow("Show Origin:", self.show_origin_check)

        layout.addWidget(visual_group)

        # Color scheme
        scheme_group = QGroupBox("Theme")
        scheme_layout = QFormLayout(scheme_group)

        self.color_scheme_combo = QComboBox()
        self.color_scheme_combo.addItems(["System", "Light", "Dark"])

        scheme_layout.addRow("Color Scheme:", self.color_scheme_combo)

        layout.addWidget(scheme_group)

        layout.addStretch()

    def load_settings(self) -> None:
        """Load current settings into UI."""
        config = config_manager.config.display

        self.grid_visible_check.setChecked(config.grid_visible)
        self.grid_size_spin.setValue(config.grid_size_mm)
        self.snap_to_grid_check.setChecked(config.snap_to_grid)

        self.units_combo.setCurrentIndex(0 if config.units == Units.MILLIMETERS else 1)
        self.decimal_places_spin.setValue(config.decimal_places)

        self._bg_color = config.background_color
        self._grid_color = config.grid_color
        self._cursor_color = config.cursor_color
        self._selection_color = config.selection_color

        self._update_color_button(self.bg_color_btn, self._bg_color)
        self._update_color_button(self.grid_color_btn, self._grid_color)
        self._update_color_button(self.cursor_color_btn, self._cursor_color)
        self._update_color_button(self.selection_color_btn, self._selection_color)

        self.antialiasing_check.setChecked(config.antialiasing)
        self.show_rulers_check.setChecked(config.show_rulers)
        self.show_origin_check.setChecked(config.show_origin)

        scheme_map = {"system": 0, "light": 1, "dark": 2}
        self.color_scheme_combo.setCurrentIndex(scheme_map.get(config.color_scheme.value, 0))

    def apply_settings(self) -> None:
        """Apply settings from UI."""
        units = Units.MILLIMETERS if self.units_combo.currentIndex() == 0 else Units.INCHES

        scheme_values = [ColorScheme.SYSTEM, ColorScheme.LIGHT, ColorScheme.DARK]
        color_scheme = scheme_values[self.color_scheme_combo.currentIndex()]

        config_manager.update_display(
            grid_visible=self.grid_visible_check.isChecked(),
            grid_size_mm=self.grid_size_spin.value(),
            snap_to_grid=self.snap_to_grid_check.isChecked(),
            units=units,
            decimal_places=self.decimal_places_spin.value(),
            background_color=self._bg_color,
            grid_color=self._grid_color,
            cursor_color=self._cursor_color,
            selection_color=self._selection_color,
            antialiasing=self.antialiasing_check.isChecked(),
            show_rulers=self.show_rulers_check.isChecked(),
            show_origin=self.show_origin_check.isChecked(),
            color_scheme=color_scheme,
        )

    def _choose_color(self, color_type: str) -> None:
        """Show color picker dialog."""
        current_map = {
            "background": self._bg_color,
            "grid": self._grid_color,
            "cursor": self._cursor_color,
            "selection": self._selection_color,
        }
        current = current_map[color_type]

        color = QColorDialog.getColor(QColor(current), self, f"Choose {color_type} color")

        if color.isValid():
            hex_color = color.name()
            if color_type == "background":
                self._bg_color = hex_color
                self._update_color_button(self.bg_color_btn, hex_color)
            elif color_type == "grid":
                self._grid_color = hex_color
                self._update_color_button(self.grid_color_btn, hex_color)
            elif color_type == "cursor":
                self._cursor_color = hex_color
                self._update_color_button(self.cursor_color_btn, hex_color)
            elif color_type == "selection":
                self._selection_color = hex_color
                self._update_color_button(self.selection_color_btn, hex_color)

    def _update_color_button(self, button: QPushButton, color: str) -> None:
        """Update button to show color."""
        button.setStyleSheet(f"background-color: {color};")
        button.setText(color)
