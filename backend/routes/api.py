import json
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
    domain_status
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

@app.route(f'{app.config["API_URI"]}/expiringDomains', methods=['GET'])
def expiringDomains():
    days = request.args.get('days')
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
            'total': len(expiring),
            'expiring_within': days,
            'expiring_domains': [domain.__dict__ for domain in expiring],
            'status_code': 200
        })

@app.route(f'{app.config["API_URI"]}/allDomains', methods=['GET'])
def allDomains():
    _order = request.args.get('order')
    if _order != 'asc' and _order != 'desc':
        return jsonify({
            'success': False,
            'status_code': 400,
            'err': 'Order must be `asc` or `desc`.'
        })
    try:
        app.logger.info(f'Expiring in {_order} order.')
        all = Domains.all_domains(order=_order)
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)
    else:
        return jsonify({
            'total': len(all),
            'order': _order,
            'domains': [domain.__dict__ for domain in all],
            'status_code': 200
        })


@app.route(f'{app.config["API_URI"]}/expiredDomains', methods=['GET'])
def expiredDomains():
    try:
        # app.logger.info(f'Expiring in {_order} order.')
        all = Domains.expired()
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)
    else:
        return jsonify({
            'total': len(all),
            'domains': [domain.__dict__ for domain in all],
            'status_code': 200
        })


@app.route(f'{app.config["API_URI"]}/liveAuction', methods=['GET'])
def liveAuction():
    try:
        all = Domains.auctions()
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)
    else:
        return jsonify({
            'total': len(all),
            'domains': [domain.__dict__ for domain in all],
            'status_code': 200
        })


@app.route(f'{app.config["API_URI"]}/allMarkets', methods=['GET'])
def allMarkets():
    _order = request.args.get('order')
    if _order != 'asc' and _order != 'desc':
        return jsonify({
            'success': False,
            'status_code': 400,
            'err': 'Order must be `asc` or `desc`.'
        })
    try:
        data = {}
        all = Markets.all_markets(order=_order)
        for markets in all:
            data[markets.__dict__['name']] = markets.__dict__
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)
    else:
        return jsonify({
            'total': len(all),
            'order': _order,
            'markets': data,
            'status_code': 200
        })


@app.route(f'{app.config["API_URI"]}/getPremium', methods=['GET'])
def refreshDomains():
    from ethereum.read_ens import get_premium

    _domain = request.args.get('domain')
    _duration = request.args.get('duration', 1)
    try:
        data = get_premium(_domain, _duration)
        # import pdb; pdb.set_trace()
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)
    else:
        return {'premium_in_eth': data}


# @app.route(f'{app.config["API_URI"]}/refreshDomains', methods=['PUT', 'PATCH'])
# def refreshDomains():
#     from ethereum.read_ens import ens_claw

#     with open(f"{app.config['WATCH_LOCATION']}.json", 'r', encoding='utf8') as outfile:
#         data = json.load(outfile)
#     import pdb; pdb.set_trace()
#     data = ens_claw(payload=data)
#     import pdb; pdb.set_trace()
#     print('SAVE MOCK INNTO DATA')


# for param in request.args:
#     if param != 'type' and param != 'page' and param !='search':
#             opportunities = opportunities.filter(
#                 getattr(Domains, param) == request.args.get(param)
#             )

# import pdb; pdb.set_trace()

# for domain in all:
#     status = domain_status(domain.expiration, domain.grace, domain.auction)
#     setattr(domain, 'status', status)
# post_to_db(domain) # Posting last one posts whole chain.