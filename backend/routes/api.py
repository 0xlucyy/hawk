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
    post_to_db,
    is_db_live,
    # domain_status,
    app,
    # db
    eip55_address_check,
)
from backend.src.scripts import (
    build_watchlist,
    populate_domains
)
import json
import secrets

from ethereum._base import Web3_Base
from siwe import SiweMessage, generate_nonce
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
        app.logger.error(f'Getting Premium ...')
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
    '''
    Generalized thegraph query'ing endpoint. 
    
    Ex./getGraphData?target=DOMAIN_ECO&domainName=lobo

    Possible targets: 
    '''
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
    # url = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={app.config["ETHERSCAN_TOKEN"]}
    url = app.config["ETHERSCAN_GET_GAS"].format(API_TOKEN=app.config['ETHERSCAN_TOKEN'])
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

    not_clean_domains = (request.form.get('addresses')).split(',')
    try:
        resp = get_reverse_record(not_clean_domains)
        app.logger.info(f"[API] resp: {resp}")
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)
    else:
        return resp

# from sqlalchemy.orm import class_mapper, object_mapper
# from sqlalchemy.orm.exc import UnmappedClassError, UnmappedInstanceError
@app.route(f'{app.config["API_URI"]}/bulkSearch', methods=['GET', 'POST'])
def bulkSearch():
    '''
    Accepts a string of domain names, seperated by commas.
    Ex. "lobo,toro,testing,r2-d2,phoenix,trashdev"
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

        # import pdb; pdb.set_trace()

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

            build_watchlist() # Read from created csv file.
            added = populate_domains() # Populate with new domains
    
            found.extend(added)
            # import pdb;pdb.set_trace()
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)
    else:
        # # Remove unwanted model fields.
        # for _domain in found:
        #     for key in not_wanted:
        #         try:
        #             del _domain.__dict__[key]
        #         except:
        #             pass
        # import pdb;pdb.set_trace()
        app.logger.info(f"[INFO] Found: {found}")

        return jsonify({
            'added': not_found,
            'invalid': invalid,
            # 'domains': [domain.__dict__ for domain in found],
            'domains': [domain.__dict__ for domain in found],
            'status_code': 200
        })

# TODO in backlog. endpt works, takes file, reads it, and returns correctly.
# frontend isnt recieving the resp tho, very weird bug.
@app.route(f'{app.config["API_URI"]}/handleSearchFile', methods=['GET', 'POST'])
def handleSearchFile():
    '''
    Accepts form txt data file. single line per work.
    '''
    bulk_seach_file = request.files.get('file')

    if bulk_seach_file.mimetype != 'text/plain':
        return {'error': 'Only text/plain files supported'}

    payload = bulk_seach_file.stream.readlines()
    domains = []
    not_printable = []

    # import pdb; pdb.set_trace()
    # TODO Check for file type
    # TODO Check for file size

    try:
        for domain in payload:
            domain = domain.decode("utf-8").replace('\n', '').strip()
            domain = json.dumps(domain, ensure_ascii=False).replace('"', "")
            if domain.isprintable() == True:
                domains.append(domain)
            else:
                not_printable.append(domain)
                app.logger.warning(f"[WARN] {domain} is not printable ...")
    except(Exception) as e:
        app.logger.error(f'Error: {e}')
        return log_error(error=e)

    # try:
    #     resp = get_reverse_record(data)
    #     app.logger.info(f"[API] resp: {resp}")
    # except(Exception) as e:
    #     app.logger.error(f'Error: {e}')
    #     return log_error(error=e)
    # else:
    return {'status_code': 200, 'domains': domains, "invalid": not_printable}


@app.route(f'{app.config["API_URI"]}/siwe', methods=['POST'])
def siwe():
    '''
    
    '''
    mainner_provider = Web3_Base()
    data = request.json

    message = SiweMessage(message=data['api_message'])
    app.logger.warning(f"[INFO] Validating {message.address} signature...")

    try:
        test = message.verify(
            signature=data['signature'],
            provider=mainner_provider.w3.provider,
            nonce=message.nonce,
            domain="localhost:3000"
        )
        return {'data': 'WORKING'}
    except Exception as error:
        app.logger.error(f'Error: {error}')
        return {'data': 'NOT WORKING'}


@app.route(f'{app.config["API_URI"]}/nonce', methods=['GET'])
def nonce():
    '''
    Returns a nonce
    '''
    # token = secrets.token_urlsafe()
    token = generate_nonce()
    app.logger.info(f'Nonce: {token}')
    return {'data': token}


# for domain in all:
#     status = domain_status(domain.expiration, domain.grace, domain.auction)
#     setattr(domain, 'status', status)
# post_to_db(domain) # Posting last one posts whole chain.