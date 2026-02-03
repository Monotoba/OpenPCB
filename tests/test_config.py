"""Tests for configuration system."""

import tempfile
import threading
from pathlib import Path

import pytest

from openpcb.config import (
    ColorScheme,
    ConfigManager,
    DisplaySettings,
    OpenPCBConfig,
    Units,
    config_manager,
    get_preset,
)


def test_config_defaults():
    """Test default configuration values."""
    config = OpenPCBConfig()

    assert config.schema_version == 1
    assert config.display.units == Units.MILLIMETERS
    assert config.hidpi.enable_high_dpi_scaling is True
    assert config.application.window_geometry.width == 1280
    assert config.workspace.show_layer_panel is True


def test_config_validation_grid_size():
    """Test pydantic validation for grid size."""
    # Invalid grid size (too large)
    with pytest.raises(ValueError):
        DisplaySettings(grid_size_mm=200.0)

    # Invalid grid size (zero or negative)
    with pytest.raises(ValueError):
        DisplaySettings(grid_size_mm=0.0)

    # Valid grid sizes
    DisplaySettings(grid_size_mm=0.1)
    DisplaySettings(grid_size_mm=100.0)


def test_config_validation_colors():
    """Test pydantic validation for hex colors."""
    # Invalid color format
    with pytest.raises(ValueError):
        DisplaySettings(background_color="not-a-color")

    with pytest.raises(ValueError):
        DisplaySettings(background_color="#gggggg")

    with pytest.raises(ValueError):
        DisplaySettings(background_color="123456")  # Missing #

    # Valid colors
    DisplaySettings(background_color="#123456")
    DisplaySettings(background_color="#abc")  # Short form
    DisplaySettings(background_color="#FFFFFF")  # Uppercase (will be lowercased)


def test_config_validation_ranges():
    """Test pydantic validation for numeric ranges."""
    # Zoom out of range
    with pytest.raises(ValueError):
        DisplaySettings(zoom_default=0.0)

    with pytest.raises(ValueError):
        DisplaySettings(zoom_default=11.0)

    # Valid zoom
    DisplaySettings(zoom_default=1.0)
    DisplaySettings(zoom_default=5.0)

    # Decimal places out of range
    with pytest.raises(ValueError):
        DisplaySettings(decimal_places=-1)

    with pytest.raises(ValueError):
        DisplaySettings(decimal_places=10)

    # Valid decimal places
    DisplaySettings(decimal_places=0)
    DisplaySettings(decimal_places=6)


def test_config_frozen():
    """Test that models are immutable (frozen)."""
    config = OpenPCBConfig()

    # Attempting to modify should raise an error
    with pytest.raises(Exception):  # Pydantic raises ValidationError or similar
        config.schema_version = 2  # type: ignore

    with pytest.raises(Exception):
        config.display.grid_visible = False  # type: ignore


def test_config_serialization():
    """Test JSON serialization roundtrip."""
    config = OpenPCBConfig()

    # Dump to dict
    data = config.model_dump_json_safe()

    # Verify data structure
    assert "schema_version" in data
    assert "application" in data
    assert "display" in data
    assert "hidpi" in data
    assert "workspace" in data

    # Load from dict
    loaded = OpenPCBConfig.model_validate_json_safe(data)

    # Verify equality
    assert loaded == config


def test_config_serialization_with_bytes():
    """Test serialization with bytes field (dock_layout)."""
    from openpcb.config.models import WorkspaceSettings

    # Create config with dock layout
    workspace = WorkspaceSettings(dock_layout=b"test_dock_layout")
    config = OpenPCBConfig(workspace=workspace)

    # Dump to dict (should base64 encode bytes)
    data = config.model_dump_json_safe()
    assert isinstance(data["workspace"]["dock_layout"], str)  # Base64 string

    # Load from dict
    loaded = OpenPCBConfig.model_validate_json_safe(data)
    assert loaded.workspace.dock_layout == b"test_dock_layout"


def test_config_manager_singleton():
    """Test ConfigManager is a singleton."""
    manager1 = ConfigManager()
    manager2 = ConfigManager()

    assert manager1 is manager2
    assert manager1 is config_manager


def test_config_manager_persistence():
    """Test config manager save/load."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create manager with temp directory
        manager = ConfigManager()
        manager._config_dir = Path(tmp_dir)
        manager._config_file = Path(tmp_dir) / "settings.json"

        # Update and save
        manager.update_display(grid_visible=False, grid_size_mm=2.5)

        # Verify file exists
        assert manager._config_file.exists()

        # Create new manager (should load from disk)
        manager2 = ConfigManager()
        manager2._config_dir = Path(tmp_dir)
        manager2._config_file = Path(tmp_dir) / "settings.json"
        manager2._config = None  # Force reload

        loaded_config = manager2.load()
        assert loaded_config.display.grid_visible is False
        assert loaded_config.display.grid_size_mm == 2.5


def test_config_manager_update_methods():
    """Test config manager update methods."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        manager = ConfigManager()
        manager._config_dir = Path(tmp_dir)
        manager._config_file = Path(tmp_dir) / "settings.json"

        # Test update_display
        manager.update_display(units=Units.INCHES, decimal_places=4)
        assert manager.config.display.units == Units.INCHES
        assert manager.config.display.decimal_places == 4

        # Test update_hidpi
        manager.update_hidpi(custom_scale_factor=2.0)
        assert manager.config.hidpi.custom_scale_factor == 2.0

        # Test update_workspace
        manager.update_workspace(active_profile="custom")
        assert manager.config.workspace.active_profile == "custom"

        # Test update_application
        manager.update_application(autosave_enabled=False)
        assert manager.config.application.autosave_enabled is False


def test_config_manager_reset():
    """Test config manager reset to defaults."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        manager = ConfigManager()
        manager._config_dir = Path(tmp_dir)
        manager._config_file = Path(tmp_dir) / "settings.json"

        # Make changes
        manager.update_display(grid_visible=False)
        assert manager.config.display.grid_visible is False

        # Reset to defaults
        manager.reset_to_defaults()
        assert manager.config.display.grid_visible is True


def test_config_thread_safety():
    """Test thread-safe access to config."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        manager = ConfigManager()
        manager._config_dir = Path(tmp_dir)
        manager._config_file = Path(tmp_dir) / "settings.json"

        errors = []

        def update_config(value: float):
            try:
                for i in range(20):
                    manager.update_display(grid_size_mm=value + (i * 0.01))
            except Exception as e:
                errors.append(e)

        # Create 10 threads updating config concurrently
        threads = [threading.Thread(target=update_config, args=(float(i),)) for i in range(10)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        # Should complete without errors
        assert len(errors) == 0

        # Config should be valid
        assert manager.config.display.grid_size_mm > 0


def test_presets():
    """Test configuration presets."""
    # Test default preset
    default = get_preset("default")
    assert default is not None
    assert default.display.color_scheme == ColorScheme.SYSTEM

    # Test light theme
    light = get_preset("light")
    assert light is not None
    assert light.display.color_scheme == ColorScheme.LIGHT
    assert light.display.background_color == "#ffffff"

    # Test high contrast
    high_contrast = get_preset("high-contrast")
    assert high_contrast is not None
    assert high_contrast.display.background_color == "#000000"
    assert high_contrast.display.antialiasing is False

    # Test 4K preset
    preset_4k = get_preset("4k")
    assert preset_4k is not None
    assert preset_4k.hidpi.custom_scale_factor == 2.0
    assert preset_4k.hidpi.toolbar_icon_size == 32

    # Test invalid preset
    invalid = get_preset("nonexistent")
    assert invalid is None


def test_atomic_writes():
    """Test that config saves are atomic (via temp file)."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        manager = ConfigManager()
        manager._config_dir = Path(tmp_dir)
        manager._config_file = Path(tmp_dir) / "settings.json"

        # Save config
        manager.update_display(grid_visible=False)

        # Verify temp file was used (check that only final file exists)
        assert manager._config_file.exists()
        assert not (Path(tmp_dir) / "settings.tmp").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
