import json
import sys
from xml import dom
from MySQLdb import _mysql
from backend.utils.utils import (
    apply_hashes_to_payload,
    tilde_identifier,
    remove_accents,
    post_to_db,
    app
)
from ethereum.read_ens import ens_claw
from backend.models import models
from sqlalchemy.exc import IntegrityError
from backend.utils.exceptions import (
    DomainModelDataTypeError
)
# import pdb; pdb.set_trace()


def populate_db():
    with open(f"{app.config['WATCH_LOCATION']}.json", 'r', encoding='utf8') as outfile:
        payload = json.load(outfile)
    
    failed = []
    index = 0
    for domain, domain_metadata in payload.items():
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
        index += 1
    app.logger.info(f"Total success: {index} - " \
                    f"Total failed: {len(failed)}" \
                    f" - {failed}")


def build_watchlist():
    '''
    Creates a json file of domains with metadata at WATCH_LOCATION.

    Full Run Cycle
    First  - Run `clean` to create `watch_clean.txt` from `watch.txt`.
    Second - Run `node ethereum/normalize.js >> watchlists/watch_clean.csv` for csv of hashes.
    Third  - Run `build_watchlist` to create `watch_clean.json`.
    '''
    payload = {}
    # Dumps WATCH_LOCATION.csv into payload - Domain name & domain hash.
    payload = apply_hashes_to_payload(payload)
    payload = ens_claw(payload)
    # import pdb; pdb.set_trace()
    with open(f"{app.config['WATCH_LOCATION']}.json", 'w', encoding='utf8') as outfile:
        # import pdb; pdb.set_trace()
        json.dump(payload, outfile, indent=4, sort_keys=True, ensure_ascii=False, default=str)


def clean_file(file: str = None):
    '''
        Creates a file without new lines, white spaces,
        lower cased, & alphanumerical ordered.

        Default location is `/watchlists/watch.txt.

        Run `clean_file watch` in terminal.
    '''
    if file == None:
        file = sys.argv[1]
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

    # #Closing the connection
    db_connection.close()
