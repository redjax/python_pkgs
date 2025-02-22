from __future__ import annotations

from dynaconf import Dynaconf

GITHUB_SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="GH",
    settings_files=["settings.toml", ".secrets.toml"],
)
