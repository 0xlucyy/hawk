from app import app#, db
from sqlalchemy.sql import text
from backend.utils.exceptions import (
    DatabaseError
)

# import pdb; pdb.set_trace()


def post_to_db(db, data):
    db.session.add(data)
    db.session.commit()
    app.logger.info(f"{data} inserted into db.")

def is_db_live(db):
    try:
        conn = db.engine.execute(text("SELECT 1"))
        return conn.connection._still_open_and_dbapi_connection_is_valid
    except:
        raise DatabaseError