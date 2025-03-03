from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger(__name__)

import sqlalchemy as sa
import sqlalchemy.orm as so

__all__ = ["setup_database"]

def create_base_metadata(
    base: so.DeclarativeBase = None, engine: sa.Engine = None
) -> None:
    """Create a SQLAlchemy base object's table metadata.

    Params:
        base (sqlalchemy.orm.DeclarativeBase): A SQLAlchemy `DeclarativeBase` object to use for creating metadata.
    """
    if base is None:
        raise ValueError("base cannot be None")
    if engine is None:
        raise ValueError("engine cannot be None")
    if not isinstance(engine, sa.Engine):
        raise TypeError(
            f"engine must be of type sqlalchemy.Engine. Got type: ({type(engine)})"
        )

    try:
        base.metadata.create_all(bind=engine)
    except Exception as exc:
        msg = Exception(
            f"({type(exc)}) Unhandled exception creating Base metadata. Details: {exc}"
        )
        raise msg

def setup_database(
    sqla_base: so.DeclarativeBase,
    engine: sa.Engine,
) -> None:
    """Setup the database tables and metadata.

    Params:
        sqla_base (sqlalchemy.orm.DeclarativeBase): A SQLAlchemy `DeclarativeBase` object to use for creating metadata.
        engine (sqlalchemy.Engine): A SQLAlchemy `Engine` to use for database connections.
    """
    engine: sa.Engine = engine

    ## Check if the driver is SQLite
    if engine.dialect.name == "sqlite":
        ## Get the database file path from the engine's URL
        db_file_path = engine.url.database

        ## Get the parent directory of the database file
        parent_dir = Path(db_file_path).parent

        ## Check if the parent directory exists
        if not parent_dir.exists():
            ## Create the parent directory if it doesn't exist
            try:
                parent_dir.mkdir(parents=True, exist_ok=True)
            except Exception as exc:
                msg = f"({type(exc)}) Detected SQLite database, but could not create at path: {parent_dir}. Details: {exc}"
                log.error(msg)
                raise exc

    try:
        create_base_metadata(base=sqla_base, engine=engine)
    except Exception as exc:
        msg = f"({type(exc)}) Error initializing Base metadata. Details: {exc}"
        log.error(msg)
        
        raise
