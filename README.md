# Python Packages

My monorepo where I keep packages I repeatedly copy/paste into new projects, but that I don't want to publish to Pypi. Most of the files in this repository, including the [`.gitignore`](.gitignore), [`pyproject.toml`](pyproject.toml), and [`ruff.toml`](ruff.toml), can be used as a reference in other projects.

## Description

Libary code is in the [`libs/` directory](./libs/). All packages should be isolated from each other, meaning you can copy the `src/<package_name>` directory from any library package into your project to get up and running. Check each library's `pyproject.toml`'s `[dendencies]` section to see if you need to install any extra packages.

The [`scripts/` directory](./scripts/) is where I store Python scripts I plan to re-use, or self-contained (single file) modules I regularly use. For instance, the [`dump_mysql_db.py` script](./scripts/database/mysql/dump_mysql_db.py), which wraps the `mysqldump` CLI utility in a Python CLI to make saving MySQL database dumps easier.

The [`pipelines/` directory] stores CI/CD pipeline files, i.e. for Github Actions, Woodpecker CI, and/or Concourse CI (or whatever other pipelines I've used).
