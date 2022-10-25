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
    is_db_live,
)


# import pdb; pdb.set_trace()


@app.route(f'{app.config["API_URI"]}/health', methods=['GET'])
def health():
    ''' Get status of API '''
    try:
        app.logger.info('Health check point...')
        is_live = is_db_live()
        if is_live != True:
            raise DataBaseOffline
    except(DataBaseOffline) as e:
        app.logger.error('Health checkpoint failed ... DataBaseOffline')
        return log_error(error=e)
    except(DatabaseError) as e:
        app.logger.error('Health checkpoint failed ... DatabaseError')
        return log_error(error=e)
    else:
        app.logger.info('Health endpoint is live...')
        return jsonify({
            'live': True,
            'status_code': 200,
            # 'content-type': 'application/json'
        })


@app.route(f'{app.config["API_URI"]}/expiring', methods=['GET'])
def get_expiring():
    days = request.args.get('days')

    '''  '''
    try:
        app.logger.info(f'Expiring over the next {days} days.')
        expiring = Domains.expiring(int(days))
    except(Exception) as e:
        app.logger.info(f'Error: {e}')
        return jsonify({
            'live': False,
            'status_code': 666,
            'content-type': 'application/json'
        })
    else:
        return jsonify({
            'total_expiring': len(expiring),
            'expiring_within': days,
            'expiring_domains': [domain.__dict__ for domain in expiring],
            'status_code': 200
        })

@app.route('/test', methods=['GET'])
def get_Test():
        return jsonify({'working': False})

# for param in request.args:
#     if param != 'type' and param != 'page' and param !='search':
#             opportunities = opportunities.filter(
#                 getattr(ENS, param) == request.args.get(param)
#             )