"""
Main window for OpenPCB application.

Provides the primary UI with menu bar, toolbars, dock widgets, and status bar.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QDockWidget,
    QFileDialog,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from PySide6.QtGui import QCloseEvent

from openpcb.config import config_manager

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window for OpenPCB.

    Provides:
    - Menu bar with File, Edit, View, Tools, Help menus
    - Toolbar with common actions
    - Dock widgets for layers, properties, tools
    - Central widget for viewer (placeholder in Phase 1)
    - Status bar with coordinates and messages
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize main window."""
        super().__init__(parent)

        self.setWindowTitle("OpenPCB")

        # Load window geometry from config
        self._restore_geometry()

        # Setup UI components
        self._create_central_widget()
        self._create_dock_widgets()
        self._create_actions()
        self._create_menus()
        self._create_toolbars()
        self._create_status_bar()

        logger.info("Main window initialized")

    def _restore_geometry(self) -> None:
        """Restore window geometry from config."""
        config = config_manager.config
        geom = config.application.window_geometry

        self.setGeometry(geom.x, geom.y, geom.width, geom.height)

        if geom.maximized:
            self.showMaximized()

    def _save_geometry(self) -> None:
        """Save window geometry to config."""
        geom = self.geometry()

        from openpcb.config.models import WindowGeometry

        new_geom = WindowGeometry(
            x=geom.x(),
            y=geom.y(),
            width=geom.width(),
            height=geom.height(),
            maximized=self.isMaximized(),
        )

        config_manager.update_application(window_geometry=new_geom)

    def _create_central_widget(self) -> None:
        """Create central widget (viewer placeholder)."""
        central = QWidget()
        layout = QVBoxLayout(central)

        # Placeholder for Phase 2 Qt Quick viewer
        label = QLabel("OpenPCB Viewer\n\n(Qt Quick scene will be integrated in Phase 2)")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("QLabel { color: #888; font-size: 14pt; }")

        layout.addWidget(label)
        self.setCentralWidget(central)

    def _create_dock_widgets(self) -> None:
        """Create dock widgets for panels."""
        # Layer panel (left)
        self.layer_dock = QDockWidget("Layers", self)
        self.layer_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        layer_widget = QLabel("Layer panel\n(Phase 2)")
        layer_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layer_dock.setWidget(layer_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.layer_dock)

        # Properties panel (right)
        self.properties_dock = QDockWidget("Properties", self)
        self.properties_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        props_widget = QLabel("Properties panel\n(Phase 2)")
        props_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.properties_dock.setWidget(props_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_dock)

        # Tool panel (left, below layers)
        self.tool_dock = QDockWidget("Tools", self)
        self.tool_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        tool_widget = QLabel("Tool panel\n(Phase 2)")
        tool_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tool_dock.setWidget(tool_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.tool_dock)

        # Restore visibility from config
        config = config_manager.config.workspace
        self.layer_dock.setVisible(config.show_layer_panel)
        self.properties_dock.setVisible(config.show_properties_panel)
        self.tool_dock.setVisible(config.show_tool_panel)

    def _create_actions(self) -> None:
        """Create QActions for menus and toolbars."""
        # File actions
        self.action_new = QAction("&New Project", self)
        self.action_new.setShortcut(QKeySequence.StandardKey.New)
        self.action_new.setStatusTip("Create a new project")
        self.action_new.triggered.connect(self._on_new_project)

        self.action_open = QAction("&Open Project...", self)
        self.action_open.setShortcut(QKeySequence.StandardKey.Open)
        self.action_open.setStatusTip("Open an existing project")
        self.action_open.triggered.connect(self._on_open_project)

        self.action_save = QAction("&Save Project", self)
        self.action_save.setShortcut(QKeySequence.StandardKey.Save)
        self.action_save.setStatusTip("Save current project")
        self.action_save.triggered.connect(self._on_save_project)

        self.action_preferences = QAction("&Preferences...", self)
        self.action_preferences.setShortcut(QKeySequence.StandardKey.Preferences)
        self.action_preferences.setStatusTip("Configure application settings")
        self.action_preferences.triggered.connect(self._on_preferences)

        self.action_quit = QAction("&Quit", self)
        self.action_quit.setShortcut(QKeySequence.StandardKey.Quit)
        self.action_quit.setStatusTip("Exit application")
        self.action_quit.triggered.connect(self.close)

        # View actions
        self.action_zoom_in = QAction("Zoom &In", self)
        self.action_zoom_in.setShortcut(QKeySequence.StandardKey.ZoomIn)
        self.action_zoom_in.triggered.connect(self._on_zoom_in)

        self.action_zoom_out = QAction("Zoom &Out", self)
        self.action_zoom_out.setShortcut(QKeySequence.StandardKey.ZoomOut)
        self.action_zoom_out.triggered.connect(self._on_zoom_out)

        self.action_zoom_fit = QAction("Zoom to &Fit", self)
        self.action_zoom_fit.setShortcut(QKeySequence("Ctrl+0"))
        self.action_zoom_fit.triggered.connect(self._on_zoom_fit)

    def _create_menus(self) -> None:
        """Create menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.action_new)
        file_menu.addAction(self.action_open)
        file_menu.addAction(self.action_save)
        file_menu.addSeparator()
        file_menu.addAction(self.action_preferences)
        file_menu.addSeparator()
        file_menu.addAction(self.action_quit)

        # Edit menu (placeholder)
        edit_menu = menubar.addMenu("&Edit")

        # View menu
        view_menu = menubar.addMenu("&View")
        view_menu.addAction(self.action_zoom_in)
        view_menu.addAction(self.action_zoom_out)
        view_menu.addAction(self.action_zoom_fit)
        view_menu.addSeparator()

        # Dock visibility toggles
        view_menu.addAction(self.layer_dock.toggleViewAction())
        view_menu.addAction(self.properties_dock.toggleViewAction())
        view_menu.addAction(self.tool_dock.toggleViewAction())

        # Tools menu (placeholder)
        tools_menu = menubar.addMenu("&Tools")

        # Help menu (placeholder)
        help_menu = menubar.addMenu("&Help")

    def _create_toolbars(self) -> None:
        """Create toolbars."""
        # Main toolbar
        main_toolbar = QToolBar("Main", self)
        main_toolbar.setObjectName("main_toolbar")
        main_toolbar.addAction(self.action_new)
        main_toolbar.addAction(self.action_open)
        main_toolbar.addAction(self.action_save)
        main_toolbar.addSeparator()
        main_toolbar.addAction(self.action_zoom_in)
        main_toolbar.addAction(self.action_zoom_out)
        main_toolbar.addAction(self.action_zoom_fit)

        # Set icon size from config
        config = config_manager.config.hidpi
        main_toolbar.setIconSize(QSize(config.toolbar_icon_size, config.toolbar_icon_size))

        self.addToolBar(main_toolbar)

    def _create_status_bar(self) -> None:
        """Create status bar."""
        status = QStatusBar()
        self.setStatusBar(status)
        status.showMessage("Ready")

    # Action handlers

    def _on_new_project(self) -> None:
        """Handle New Project action."""
        logger.info("New project requested")
        self.statusBar().showMessage("New project (Phase 2)", 3000)

    def _on_open_project(self) -> None:
        """Handle Open Project action."""
        logger.info("Open project requested")

        config = config_manager.config
        last_dir = config.workspace.last_project_directory or ""

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", last_dir, "OpenPCB Projects (*.openpcb.json);;All Files (*)"
        )

        if file_path:
            logger.info(f"Selected project: {file_path}")
            # Update last directory
            from pathlib import Path

            config_manager.update_workspace(last_project_directory=str(Path(file_path).parent))

    def _on_save_project(self) -> None:
        """Handle Save Project action."""
        logger.info("Save project requested")
        self.statusBar().showMessage("Save project (Phase 2)", 3000)

    def _on_preferences(self) -> None:
        """Handle Preferences action."""
        logger.info("Opening preferences dialog")

        from openpcb.ui.preferences import PreferencesDialog

        dialog = PreferencesDialog(self)
        dialog.exec()

    def _on_zoom_in(self) -> None:
        """Handle Zoom In action."""
        logger.debug("Zoom in")
        self.statusBar().showMessage("Zoom in (Phase 2)", 2000)

    def _on_zoom_out(self) -> None:
        """Handle Zoom Out action."""
        logger.debug("Zoom out")
        self.statusBar().showMessage("Zoom out (Phase 2)", 2000)

    def _on_zoom_fit(self) -> None:
        """Handle Zoom to Fit action."""
        logger.debug("Zoom to fit")
        self.statusBar().showMessage("Zoom to fit (Phase 2)", 2000)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle window close event."""
        logger.info("Closing main window")

        # Save window geometry
        self._save_geometry()

        # Save dock visibility
        config_manager.update_workspace(
            show_layer_panel=self.layer_dock.isVisible(),
            show_properties_panel=self.properties_dock.isVisible(),
            show_tool_panel=self.tool_dock.isVisible(),
        )

        event.accept()
