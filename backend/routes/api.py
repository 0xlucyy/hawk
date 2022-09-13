from app import (
    app,
    db
)
from flask import (
    request,
    jsonify
)
from sqlalchemy.sql import text
from backend.utils.exceptions import (
    ProviderMissing,
    ProviderOffline,
    DataBaseOffline,
    log_error
)
from config import _Base


@app.route(f'{app.config["API_URI"]}/health', methods=['GET'])
def health():
    ''' Get status of API '''
    try:
        # import pdb; pdb.set_trace()
        conn = db.engine.execute(text("SELECT 1"))
        is_live = conn.connection._still_open_and_dbapi_connection_is_valid
        if is_live != True:
            raise DataBaseOffline
    except (Exception) as error:
        return log_error(error)
    else:
        return jsonify({
            'live': True,
            'status_code': 200
        })