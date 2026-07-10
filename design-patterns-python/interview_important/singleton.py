"""
** Singleton Pattern (Interview Important)
When to use:
- When exactly one instance of a class is needed to coordinate actions across the system
- When you need strict global access to a shared resource
- When you want to control concurrent access to a shared resource

Real-world examples:
- Django settings: django.conf.settings is a singleton that lazily loads settings module
- Python logging: logging.getLogger(name) returns the same Logger instance for a given name
- Database connection pools: sqlalchemy create_engine returns the same Engine for identical URLs
- Python's import system: Modules are singletons — imported once, shared everywhere
- Flask's current_app proxy: points to the single application instance per request context
"""

from __future__ import annotations

import os
import json
import threading
import configparser
from typing import Any, Optional
from pathlib import Path


class ConfigurationManager:
    """
    Thread-safe singleton configuration manager.

    Reads configuration from a JSON file and environment variables.
    Environment variables take precedence over file values.
    """

    _instance: Optional[ConfigurationManager] = None
    _lock: threading.Lock = threading.Lock()
    _initialized: bool = False

    def __new__(cls, *args, **kwargs) -> ConfigurationManager:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_path: Optional[str] = None) -> None:
        if self._initialized:
            return
        with self._lock:
            if self._initialized:
                return
            self._config_path = config_path
            self._data: dict[str, Any] = {}
            self._env_prefix = "APP_"
            self._load_config()
            self._initialized = True

    def _load_config(self) -> None:
        if self._config_path and Path(self._config_path).exists():
            with open(self._config_path, encoding="utf-8") as f:
                file_config = json.load(f)
            self._deep_merge(self._data, file_config)
        loaded = self._load_env_vars()
        self._deep_merge(self._data, loaded)

    def _load_env_vars(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in os.environ.items():
            if key.startswith(self._env_prefix):
                config_key = key[len(self._env_prefix):].lower()
                result[config_key] = self._coerce_value(value)
        return result

    @staticmethod
    def _coerce_value(value: str) -> Any:
        lower = value.lower()
        if lower in ("true", "yes", "1"):
            return True
        if lower in ("false", "no", "0"):
            return False
        if lower == "null" or lower == "none":
            return None
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        return value

    @staticmethod
    def _deep_merge(base: dict, overlay: dict) -> None:
        for key, value in overlay.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                ConfigurationManager._deep_merge(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self._data
        for k in keys:
            if not isinstance(value, dict):
                return default
            value = value.get(k)
            if value is None:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        keys = key.split(".")
        target = self._data
        for k in keys[:-1]:
            if k not in target or not isinstance(target[k], dict):
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value

    @property
    def database_url(self) -> str:
        return self.get("database.url", "sqlite:///default.db")

    @property
    def debug(self) -> bool:
        return self.get("debug", False)

    @property
    def secret_key(self) -> str:
        return self.get("secret_key", "unsafe-default-key")

    @property
    def allowed_hosts(self) -> list[str]:
        return self.get("allowed_hosts", ["*"])

    def reset(self) -> None:
        with self._lock:
            self._data = {}
            self._initialized = False

    def __repr__(self) -> str:
        return f"ConfigurationManager(id={id(self)}, path={self._config_path})"


class DatabaseConnectionPool:
    """Another singleton example — a simple connection pool registry."""

    _instances: dict[str, DatabaseConnectionPool] = {}
    _lock: threading.Lock = threading.Lock()
    _dsn: str = ""
    _pool_size: int = 5
    _active_connections: int = 0

    def __new__(cls, dsn: str, **kwargs) -> DatabaseConnectionPool:
        if dsn not in cls._instances:
            with cls._lock:
                if dsn not in cls._instances:
                    instance = super().__new__(cls)
                    instance._dsn = dsn
                    instance._pool_size = kwargs.get("pool_size", 5)
                    instance._active_connections = 0
                    cls._instances[dsn] = instance
        return cls._instances[dsn]

    def acquire(self) -> str:
        self._active_connections += 1
        return f"<connection:{self._dsn}:{self._active_connections}>"

    def release(self, conn: str) -> None:
        self._active_connections -= 1

    @property
    def dsn(self) -> str:
        return self._dsn

    def __repr__(self) -> str:
        return f"DBPool(dsn={self._dsn}, active={self._active_connections}, size={self._pool_size})"


if __name__ == "__main__":
    import tempfile

    config_data = {
        "app_name": "MyApp",
        "debug": False,
        "database": {
            "url": "postgresql://localhost:5432/myapp",
            "pool_size": 10,
        },
        "allowed_hosts": ["localhost", "127.0.0.1"],
        "features": {
            "analytics": True,
            "beta": False,
        },
    }

    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(config_data, tmp)
    tmp.close()

    os.environ["APP_SECRET_KEY"] = "super-secret-env-key-4242"
    os.environ["APP_DEBUG"] = "true"
    os.environ["APP_FEATURES_BETA"] = "true"

    cfg1 = ConfigurationManager(tmp.name)
    cfg2 = ConfigurationManager()

    print("=== Singleton Verification ===")
    print(f"  cfg1 is cfg2: {cfg1 is cfg2}")
    print(f"  cfg1 == cfg2: {id(cfg1) == id(cfg2)}")
    print()

    print("=== Configuration Values ===")
    print(f"  app_name:       {cfg1.get('app_name')}")
    print(f"  debug:          {cfg1.debug}")
    print(f"  secret_key:     {cfg1.secret_key}")
    print(f"  database.url:   {cfg1.database_url}")
    print(f"  database.pool_size: {cfg1.get('database.pool_size')}")
    print(f"  allowed_hosts:  {cfg1.allowed_hosts}")
    print(f"  features.beta:  {cfg1.get('features.beta')}")
    print()

    print("=== Thread Safety Demo ===")
    results = []

    def worker(thread_id: int) -> None:
        cfg = ConfigurationManager()
        cfg.set(f"thread_{thread_id}_config", f"data-from-thread-{thread_id}")
        results.append(f"Thread {thread_id}: cfg={id(cfg)}, value={cfg.get(f'thread_{thread_id}_config')}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for r in results:
        print(f"  {r}")
    print()

    print("=== Database Connection Pool Singleton ===")
    pool1 = DatabaseConnectionPool("postgresql://localhost/mydb", pool_size=5)
    pool2 = DatabaseConnectionPool("postgresql://localhost/mydb", pool_size=20)
    pool3 = DatabaseConnectionPool("mysql://localhost/other", pool_size=3)

    print(f"  pool1 is pool2: {pool1 is pool2}")
    print(f"  pool1: {pool1}")
    print(f"  pool3: {pool3}")

    conn = pool1.acquire()
    print(f"  Acquired: {conn}")
    pool1.release(conn)

    Path(tmp.name).unlink(missing_ok=True)

