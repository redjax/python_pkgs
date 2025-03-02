# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "database-lib",
# ]
#
# [tool.uv.sources]
# database-lib = { path = "../../libs/database-lib" }
# ///
from __future__ import annotations

import db_lib
from loguru import logger as log
import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import sqlalchemy.orm as so

if __name__ == "__main__":
    log.info("db_lib sandbox")

    sqla_base: so.DeclarativeBase = db_lib.Base
    log.info("Creating in-memory SQLite database engine")
    try:
        engine: sa.Engine = db_lib.get_engine(url="sqlite:///:memory:", echo=True)
    except Exception as exc:
        msg = f"({type(exc)}) Error creating in-memory SQLite database engine. Details: {exc}"
        log.error(msg)
        
        raise
    
    class PersonModel(sqla_base, db_lib.TimestampMixin):
        __tablename__ = "people"
        
        id: so.Mapped[db_lib.annotated.INT_PK]
        
        name: so.Mapped[str] = so.mapped_column(sa.VARCHAR(255), nullable=False, unique=True)
        age: so.Mapped[int] = so.mapped_column(sa.NUMERIC, nullable=False, unique=False)
        email: so.Mapped[str] = so.mapped_column(sa.VARCHAR(255), nullable=True, unique=True)
    
    log.info("Initializing list of PersonModel entities")
    people: list[PersonModel] = [
        PersonModel(name="Polly", age=15, email="polly@wantsacracker.org"),
        PersonModel(name="Jeffrey", age=30, email="jeffrey@shyeahboi.com"),
        PersonModel(name="Cynthia", age=60)
    ]
    
    log.info("Creating base metadata")
    try:
        db_lib.create_base_metadata(base=sqla_base, engine=engine)
    except Exception as exc:
        msg = f"({type(exc)}) Error creating Base metadata. Details: {exc}"
        log.error(msg)
        
        raise
    
    log.info("Printing table names")
    try:
        db_lib.show_table_names(engine=engine)
    except Exception as exc:
        msg = f"({type(exc)}) Error printing table names. Details: {exc}"
        log.error(msg)
        
        raise

    log.info("Initializing session pool")
    try:
        session_pool = db_lib.get_session_pool(engine=engine)
    except Exception as exc:
        msg = f"({type(exc)}) Unable to initialize session pool. Details: {exc}"
        log.error(msg)
        
        raise
    
    log.info("Saving entities to database")
    try:
        with session_pool() as session:
            session.add_all(people)
            session.flush()
            session.commit()
    except Exception as exc:
        msg = f"({type(exc)}) Error saving entities to database. Details: {exc}"
        log.error(msg)
        
        raise
    
    log.info("Counting rows in table: people")
    try:
        row_count = db_lib.count_table_rows(table="people", engine=engine)
        log.info(f"Counted [{row_count}] row(s) in table: people.")
    except Exception as exc:
        msg = f"({type(exc)}) Error counting rows in table: people. Details: {exc}"
        log.error(msg)
        
        raise
    
    log.info("Showing all entries")
    try:
        with session_pool() as session:
            for _person in session.scalars(sa.select(PersonModel)):
                log.info(f"Found person: {_person.__dict__}")
    except Exception as exc:
        msg = f"({type(exc)}) Error showing all entries. Details: {exc}"
        log.error(msg)
        
        raise