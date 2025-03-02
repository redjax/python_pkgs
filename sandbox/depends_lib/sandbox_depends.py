# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "database-lib",
#     "depends-lib",
#     "dynaconf",
#     "loguru",
#     "settings-lib",
#     "sqlalchemy",
# ]
#
# [tool.uv.sources]
# database-lib = { path = "../../libs/database-lib" }
# settings-lib = { path = "../../libs/settings-lib" }
# depends-lib = { path = "../../libs/depends-lib" }
# ///

from loguru import logger as log

from depends import db_depends
import db_lib
from settings import db_settings

import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.exc as sa_exc

if __name__ == "__main__":
    log.info("Start depends sandbox")
    
    db_uri: sa.URL = db_depends.get_db_uri()
    log.info(f"Database URI: {db_uri}")
    
    engine: sa.Engine = db_depends.get_db_engine(db_uri=db_uri, echo=True)
    log.info(f"Database engine: {engine}")
    
    session_pool: so.scoped_session = db_depends.get_session_pool(engine=engine)
    log.info(f"Database session pool: {session_pool}")