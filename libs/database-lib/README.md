# Database lib

A library for working with `sqlalchemy` and databases. This package scaffolds the required `sqlalchemy` setup, like creating a [`Base` object](./src/db_lib/base.py), adds pre-built [SQLAlchemy type annotations](./src/db_lib/annotated.py), and adding [utility functions](./src/db_lib/utils.py) to assist with building database URI connection strings, and returning a SQLAlchemy `Engine` object.
