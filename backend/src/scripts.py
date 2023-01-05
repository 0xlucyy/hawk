import subprocess
import json
import sys
import time
from xml import dom
from datetime import datetime
from MySQLdb import _mysql
from backend.utils.utils import (
    apply_hashes_to_payload,
    tilde_identifier,
    remove_accents,
    post_to_db,
    app,
    db
)
from ethereum.read_ens import ens_claw, ens_claw_update_domains
from backend.models import models
from sqlalchemy.exc import IntegrityError
from backend.utils.exceptions import (
    DomainModelDataTypeError
)
# import pdb; pdb.set_trace()


def populate_markets():
    with open(f"backend/utils/markets.json", 'r', encoding='utf8') as outfile:
        payload = json.load(outfile)

    failed = []
    index = 0
    for market, market_metadata in payload.items():
        try:
            new_market = models.Markets(**market_metadata)
        except DomainModelDataTypeError as DMDTE:
            app.logger.error(DMDTE)
            failed.append(market)
            continue
        try:
            post_to_db(new_market)
        except IntegrityError as IE: # DB duplicate collision
            app.logger.error(IE)
            failed.append(market)
            continue
        index += 1
    app.logger.info(f"Total success: {index} - " \
                    f"Total failed: {len(failed)}" \
                    f" - {failed}")

def populate_domains(file: str = app.config['WATCH_LOCATION']):
    '''
    Assumes all domains are not in db.
    '''
    with open(f"{file}.json", 'r', encoding='utf8') as outfile:
        payload = json.load(outfile)
    
    added = []
    failed = []
    for domain, domain_metadata in payload.items():
        # import pdb; pdb.set_trace()
        try:
            new_domain = models.Domains(**domain_metadata)
        except DomainModelDataTypeError as DMDTE:
            app.logger.error(DMDTE)
            failed.append(domain)
            continue

        try:
            post_to_db(new_domain)
        except IntegrityError as IE: # DB duplicate collision
            app.logger.error(IE)
            failed.append(domain)
            continue
        added.append(new_domain)
    app.logger.info(f"Total success: {len(added)} - " \
                    f"Total failed: {len(failed)}" \
                    f" - {failed}")
    return added

def build_watchlist():
    '''
    Creates a json file of domains with metadata at WATCH_LOCATION
    ie /watchlists/watch_clean.json.

    payload is an object which, at most, contains all columns in
    model Domains as key values in the dictionary.
    if a key value is added to the payload object which is not a
    column in model Domains, populate_domains() will fail.
    '''
    payload = {}
    # Dumps WATCH_LOCATION.csv into payload - Domain name & domain hash.
    payload = apply_hashes_to_payload(payload)
    payload = ens_claw(payload)
    with open(f"{app.config['WATCH_LOCATION']}.json", 'w', encoding='utf8') as outfile:
        json.dump(payload, outfile, indent=4, sort_keys=True, ensure_ascii=False, default=str)


def clean_file(file: str = None):
    '''
        Creates a file without new lines, white spaces,
        lower cased, & alphanumerical ordered.

        Default location is `/watchlists/watch.txt.

        Run `clean_file watch` in terminal.
    '''
    if file == None:
        try:
            file = sys.argv[1]
        except Exception as e:
            file = 'watch'
    app.logger.info(f"Reading {app.config['DOMAIN_WATCH_FOLDER']}/{file}.txt ...")

    # Read from uncleaned file.
    with open(f"{app.config['DOMAIN_WATCH_FOLDER']}/{file}.txt", 'r') as f:
        words = f.readlines()

    clean = []
    for word in words:
        word = word.replace('\n', "").lower()
        word = word.replace(' ', "")
        clean.append(word)
        if tilde_identifier(word) == True:
            non_tilde_copy = remove_accents(word)
            clean.append(non_tilde_copy.replace('\n', ""))

    app.logger.info(f"Cleaned ...")
    clean.sort()
    clean = list(dict.fromkeys(clean))
    app.logger.info(f"Sorted & dedupped ...")

    f = open(f"{app.config['DOMAIN_WATCH_FOLDER']}/{file}_{app.config['CLEAN_FILE']}.txt", 'w')
    for word in clean:
        f.write(word.replace(' ', ''))
        f.writelines('\n')
    f.close()

    app.logger.info(f"Created {app.config['DOMAIN_WATCH_FOLDER']}/{file}_{app.config['CLEAN_FILE']}.txt ...")


def create_database():
    '''
    Drops & creates a new database depending on ENV setting.
    '''
    # establishing the connection
    db_connection = _mysql.connect(user=app.config['MYSQL_USERNAME'], password=app.config['MYSQL_PASSWORD'], host='127.0.0.1')

    app.logger.info(f"Dropping {app.config['MYSQL_DB']} database...")

    # Doping database MYDATABASE if already exists.
    db_connection.query(f"DROP database IF EXISTS {app.config['MYSQL_DB']}")

    app.logger.info(f"Creating {app.config['MYSQL_DB']} database...")

    # Creating a database
    db_connection.query(f"CREATE database {app.config['MYSQL_DB']}")

    app.logger.info(f"Created {app.config['MYSQL_DB']} database...")

    # db_connection.query("SHOW DATABASES")
    # results = db_connection.use_result()

    # Creating all tables, then closing the connection.
    db.create_all()
    db_connection.close()


def clean_slate():
    '''
        Watchlist file is a single line text file.
        Default is located in /watchlist/watch.txt

        Programatic version of READ.ME ## Getting started
        section.
    '''
    start_time = time.time()
    get_hashes_cmd = 'node ethereum/normalize.js >> watchlists/watch_clean.csv'

    # Clean CSV file
    f = open(f"{app.config['WATCH_LOCATION']}.csv", "w+")
    f.close()

    clean_file()
    subprocess.run(['sh', '-c', get_hashes_cmd])
    build_watchlist()
    create_database()
    populate_domains()
    populate_markets()

    print("--- %.2f seconds ---" % (time.time() - start_time))






# TODO ensure scripts below work as intended.
def update_domains():
    '''
        Full update on domains. Default source of domains
        is watchlists/watch.txt.
    '''
    start_time = time.time()
    get_hashes_cmd = 'node ethereum/normalize.js >> watchlists/watch_clean.csv'

    clean_file()
    subprocess.run(['sh', '-c', get_hashes_cmd])
    build_watchlist()
    refresh_domains()

    print("--- %.2f seconds ---" % (time.time() - start_time))


def refresh_domains():
    '''
        Partial update on domains. Default source of domains
        is watchlists/watch_clean.json.
    '''
    start_time = time.time()
    domains = models.Domains.query.all()
    ens_claw_update_domains(domains)
    print("--- %.2f seconds ---" % (time.time() - start_time))

    # for domain in domains:
    #     app.logger.info(f"Working on {domain.name}...")
    #     try:
    #         import pdb; pdb.set_trace()
    #         ens_claw_update_domains(domain)
    #     except Exception as error:
    #         app.logger.error(error)
    #         failed += 1
    #         failed_named.append(domain.name)
    #         continue

    #     try:
    #         if domain is not None: # domain exists in db.
    #             for key in update_keys:
    #                 setattr(domain, key, payload[domain_name][key]) if key != 'expiration' else setattr(domain, key, (payload[domain_name][key]).upper())
    #             setattr(domain, '_updated_at', datetime.now())
    #             time_and_status = models.Domains.get_times_and_status(payload[domain_name]['expiration'])
    #             for key,value in time_and_status.items():
    #                 try:
    #                     setattr(domain, key, value)
    #                 except Exception as error:
    #                     print(error)
    #             post_to_db(just_commit=True)
    #             domains_updated += 1
    #         else: # domain does not exist in db.
    #             new_domain = models.Domains(**domain_metadata)
    #             post_to_db(data=new_domain)
    #             domains_createad += 1
    #     except DomainModelDataTypeError as DMDTE:
    #         app.logger.error(DMDTE)
    #         failed += 1
    #         failed_named.append(domain_name)
    # print(f"Total domains created: {domains_createad} - " \
    #                 f"Total domains updated: {domains_updated} - " \
    #                 f"Total failed: {failed}")
