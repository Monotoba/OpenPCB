"""
Configuration manager for OpenPCB.

Provides thread-safe access to application configuration with automatic
persistence to disk using orjson for performance.
"""

from __future__ import annotations

import logging
import threading
from pathlib import Path
from typing import Any

import orjson
from platformdirs import user_cache_dir, user_config_dir, user_data_dir

from .models import OpenPCBConfig

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Singleton configuration manager with thread-safe access.

    Usage:
        from openpcb.config import config_manager

        # Read settings
        zoom = config_manager.config.display.zoom_default

        # Update settings (creates new config due to frozen models)
        config_manager.update_display(grid_visible=False)

        # Save to disk
        config_manager.save()
    """

    _instance: ConfigManager | None = None
    _lock = threading.RLock()

    def __new__(cls) -> ConfigManager:
        """Ensure singleton instance."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self) -> None:
        """Initialize configuration manager."""
        # Prevent re-initialization
        if hasattr(self, "_initialized"):
            return

        self._initialized = True
        self._config: OpenPCBConfig | None = None
        self._config_lock = threading.RLock()

        # Platform-specific directories
        self._config_dir = Path(user_config_dir("openpcb", "openpcb"))
        self._cache_dir = Path(user_cache_dir("openpcb", "openpcb"))
        self._data_dir = Path(user_data_dir("openpcb", "openpcb"))

        self._config_file = self._config_dir / "settings.json"

        # Ensure directories exist
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._data_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Config directory: {self._config_dir}")
        logger.info(f"Cache directory: {self._cache_dir}")
        logger.info(f"Data directory: {self._data_dir}")

    @property
    def config(self) -> OpenPCBConfig:
        """Get current configuration (thread-safe)."""
        with self._config_lock:
            if self._config is None:
                self._config = self.load()
            return self._config

    @property
    def config_dir(self) -> Path:
        """Get configuration directory path."""
        return self._config_dir

    @property
    def cache_dir(self) -> Path:
        """Get cache directory path."""
        return self._cache_dir

    @property
    def data_dir(self) -> Path:
        """Get data directory path."""
        return self._data_dir

    def load(self) -> OpenPCBConfig:
        """Load configuration from disk or create default."""
        with self._config_lock:
            if not self._config_file.exists():
                logger.info("No config file found, creating default")
                config = OpenPCBConfig()
                self.save(config)
                return config

            try:
                data = orjson.loads(self._config_file.read_bytes())
                config = OpenPCBConfig.model_validate_json_safe(data)
                logger.info("Configuration loaded successfully")
                return config
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                logger.warning("Using default configuration")
                return OpenPCBConfig()

    def save(self, config: OpenPCBConfig | None = None) -> None:
        """Save configuration to disk."""
        with self._config_lock:
            if config is None:
                config = self._config

            if config is None:
                logger.warning("No configuration to save")
                return

            try:
                # Convert to JSON-safe dict
                data = config.model_dump_json_safe()

                # Write with orjson (faster than stdlib json)
                json_bytes = orjson.dumps(
                    data, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
                )

                # Atomic write (write to temp, then rename)
                temp_file = self._config_file.with_suffix(".tmp")
                temp_file.write_bytes(json_bytes)
                temp_file.replace(self._config_file)

                logger.info(f"Configuration saved to {self._config_file}")
            except Exception as e:
                logger.error(f"Failed to save config: {e}")
                raise

    def update_application(self, **kwargs: Any) -> None:
        """Update application settings."""
        with self._config_lock:
            current = self.config.application
            updated = current.model_copy(update=kwargs)
            self._config = self.config.model_copy(update={"application": updated})
            self.save()

    def update_display(self, **kwargs: Any) -> None:
        """Update display settings."""
        with self._config_lock:
            current = self.config.display
            updated = current.model_copy(update=kwargs)
            self._config = self.config.model_copy(update={"display": updated})
            self.save()

    def update_hidpi(self, **kwargs: Any) -> None:
        """Update HiDPI settings."""
        with self._config_lock:
            current = self.config.hidpi
            updated = current.model_copy(update=kwargs)
            self._config = self.config.model_copy(update={"hidpi": updated})
            self.save()

    def update_workspace(self, **kwargs: Any) -> None:
        """Update workspace settings."""
        with self._config_lock:
            current = self.config.workspace
            updated = current.model_copy(update=kwargs)
            self._config = self.config.model_copy(update={"workspace": updated})
            self.save()

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        with self._config_lock:
            self._config = OpenPCBConfig()
            self.save()
            logger.info("Configuration reset to defaults")


# Global singleton instance
config_manager = ConfigManager()
