# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "database-lib",
#     "depends-lib",
#     "loguru",
#     "setup-lib",
#     "sqlalchemy",
# ]
#
# [tool.uv.sources]
# setup-lib = { path = "../../libs/setup-lib" }
# depends-lib = { path = "../../libs/depends-lib" }
# database-lib = { path = "../../libs/database-lib" }
# ///

from loguru import logger as log

import db_lib
from depends import db_depends
import setup

import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.exc as sa_exc

if __name__ == "__main__":
    print("Configuring logging")
    setup.setup_loguru_logging(log_level="DEBUG")
    
    log.info("Start setup_lib sandbox")
    log.debug("Test DEBUG message")
    
    sqla_base: so.DeclarativeBase = db_lib.Base
    engine = db_depends.get_db_engine(db_uri=db_depends.get_db_uri(), echo=True)
    
    class PersonModel(sqla_base, db_lib.TimestampMixin):
        __tablename__ = "people"
        
        id: so.Mapped[db_lib.annotated.INT_PK]
        
        name: so.Mapped[str] = so.mapped_column(sa.VARCHAR(255), nullable=False, unique=True)
        age: so.Mapped[int] = so.mapped_column(sa.NUMERIC, nullable=False, unique=False)
        email: so.Mapped[str] = so.mapped_column(sa.VARCHAR(255), nullable=True, unique=True)
    
    log.info("Initializing list of PersonModel entities")
    # people: list[PersonModel] = [
    #     PersonModel(name="Polly", age=15, email="polly@wantsacracker.org"),
    #     PersonModel(name="Jeffrey", age=30, email="jeffrey@shyeahboi.com"),
    #     PersonModel(name="Cynthia", age=60)
    # ]
    
    log.info("Setting up database")
    setup.setup_database(sqla_base=sqla_base, engine=engine)
    
    db_tables = db_lib.show_table_names(engine=engine)
    log.info(f"Init DB tables:\n{db_tables}")
