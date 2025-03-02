from __future__ import annotations

__all__ = ["DEMO_DB_CONFIG"]

DEMO_DB_CONFIG: dict = {
    "drivername": "sqlite+pysqlite",
    "username": None,
    "password": None,
    "host": None,
    "port": None,
    "database": ".db/demo.sqlite3",
}
