from app import (
    app,
    db
)
from flask import (
    request,
    jsonify
)
from backend.utils.exceptions import (
    ProviderMissing,
    ProviderOffline,
    DataBaseOffline,
    DatabaseError,
    log_error
)
from backend.models.models import *
from backend.utils.utils import (
    post_to_db,
    is_db_live
)
# import pdb; pdb.set_trace()


@app.route(f'{app.config["API_URI"]}/health', methods=['GET'])
def health():
    ''' Get status of API '''
    try:
        is_live = is_db_live(db)
        if is_live != True:
            raise DataBaseOffline
    except(DataBaseOffline) as e:
        return log_error(error=e)
    except(DatabaseError) as e:
        return log_error(error=e)
    else:
        return jsonify({
            'live': True,
            'status_code': 200
        })


# for param in request.args:
#     if param != 'type' and param != 'page' and param !='search':
#             opportunities = opportunities.filter(
#                 getattr(ENS, param) == request.args.get(param)
#             )