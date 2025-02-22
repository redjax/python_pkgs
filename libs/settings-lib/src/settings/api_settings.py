from __future__ import annotations

from dynaconf import Dynaconf

FASTAPI_SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="FASTAPI",
    settings_files=["settings.toml", ".secrets.toml"],
)

UVICORN_SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="UVICORN",
    settings_files=["settings.toml", ".secrets.toml"],
)
