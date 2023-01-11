import subprocess
import requests
# import json
from ethereum.read_ens import (
    get_premium,
    get_reverse_record
)
from flask import (
    request,
    jsonify
)
from backend.utils.exceptions import (
    # ProviderMissing,
    # ProviderOffline,
    DataBaseOffline,
    DatabaseError,
    log_error
)
from backend.models.models import *
from backend.utils.utils import (
    # post_to_db,
    is_db_live,
    # domain_status,
    app,
    # db
)
from backend.src.scripts import (
    build_watchlist,
    populate_domains
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
# def expiredDomainsDEL():
#     try:
#         # app.logger.info(f'Expiring in {_order} order.')
#         all = Domains.expired()
#     except(Exception) as e:
#         app.logger.error(f'Error: {e}')
#         return log_error(error=e)
#     else:
#         return jsonify({
#             'total': len(all),
#             'domains': [domain.__dict__ for domain in all],
#             'status_code': 200
#         })
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
            'domains': [domain.__dict__ for domain in expiring],
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
def getPremium():
    # from ethereum.read_ens import get_premium

    _domain = request.args.get('domain')
    _duration = request.args.get('duration', 1)
    try:
        data = get_premium(_domain, _duration)
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)
    else:
        if len(_domain) == 3:
            return {'premium_in_eth': data, 'cost_per_year': app.config["THREE_LETTER"], 'years': _duration}
        elif len(_domain) == 4:
            return {'premium_in_eth': data, 'cost_per_year': app.config["FOUR_LETTER"], 'years': _duration}
        else:
            return {'premium_in_eth': data, 'cost_per_year': app.config["MORE_THEN_FOUR_LETTERS"], 'years': _duration}


@app.route(f'{app.config["API_URI"]}/getGraphData', methods=['GET'])
def getGraphData():
    from graphql.main import make_graphql_request
    _target = request.args.get('target')
    _domainName = request.args.get('domainName')

    try:
        resp = make_graphql_request(_target, _domainName)
        resp['name'] = _domainName
        resp['queryTarget'] = _target
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)
    else:
        return resp

@app.route(f'{app.config["API_URI"]}/getETHGasCosts', methods=['GET'])
def getETHGasCosts():
    url = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={app.config["ETHERSCAN_TOKEN"]}'
    try:
        resp = requests.get(url)
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)
    else:
        return resp.json()


@app.route(f'{app.config["API_URI"]}/getReverseRecords', methods=['GET', 'POST'])
def getReverseRecords():
    # Ex of addresses: "toro,lobo,testing,domainNames"
    not_clean_addresses = (request.form.get('addresses')).split(',')

    try:
        resp = get_reverse_record(not_clean_addresses)
        app.logger.info(f"[API] resp: {resp}")
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)
    else:
        return resp


@app.route(f'{app.config["API_URI"]}/bulkSearch', methods=['GET', 'POST'])
def bulkSearch():
    '''
    Accepts a string of domain names, seperated by commas.
    Ex. "lobo,toro,testing,r2-d2"
    Returns all found domains.
    '''
    not_wanted = ['_created_at', '_last_activity_at', '_sa_instance_state', '_updated_at']
    # List of domains
    _domains = (request.form.get('domains')).split(',')

    try:
        found = []
        not_found = []
        invalid = []

        # Get domains present in db, identify domains not present.
        for _domain in _domains:
            if _domain == "": continue
            _domain = _domain.strip()

            if len(_domain) < 3:
                invalid.append(_domain)
                continue

            data = Domains.domain_exists(domain_name=_domain)
            if data == False: # Domain not in db.
                not_found.append(_domain)
            else: # Domain found in db.
                found.append(data)

        # Dedup list of not found, as a precaution.
        not_found = list(dict.fromkeys(not_found))

        app.logger.info(f"found: {found}. not_found: {not_found}")

        # If some names not present in db, add them to db.
        if len(not_found) > 0:
            # Clean CSV file - needed due to python/node interchange.
            f = open(f"{app.config['WATCH_LOCATION']}.csv", "w+")
            f.close()
            
            query_list = []
            for domain in not_found: # single quotes needed for cmd argv
                query_list.append(f"'{domain}'")

            # nameprep/ens validation on words.
            get_hashes_cmd = f"node ethereum/normalize.js {' '.join(query_list)} >> watchlists/watch_clean.csv"
            subprocess.run(['sh', '-c', get_hashes_cmd])

            build_watchlist() # Read from created json file.
            added = populate_domains() # Populate with new domains
    
            found.extend(added)
            app.logger.info(f"found 2: {found}")
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)
    else:
        # Remove unwanted model fields.
        for _domain in found:
            for key in not_wanted:
                try:
                    del _domain.__dict__[key]
                except:
                    pass
        app.logger.info(f"found 3: {found}")
        return jsonify({
            'added': not_found,
            'invalid': invalid,
            'domains': [domain.__dict__ for domain in found],
            'status_code': 200
        })


# @app.route(f'{app.config["API_URI"]}/refreshDomains', methods=['GET'])
# def refreshDomains():
#     # from ethereum.read_ens import get_premium
#     try:
#         print('test')
#     except(Exception) as e:
#         app.logger.error(f'Error: {e}')
#         return log_error(error=e)
#     else:
#         return {'test': 'data'}


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