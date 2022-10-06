import json
import sys
from MySQLdb import _mysql
from backend.utils.utils import (
    apply_hashes_to_payload,
    tilde_identifier,
    remove_accents,
    app
)
from ethereum.read_ens import ens_claw
# import pdb; pdb.set_trace()


def build_watchlist():
    '''
    Creates a json file of domains with metadata at WATCH_LOCATION.

    Full Run Cycle
    First  - Run `clean` to create `watch_clean.txt` from `watch.txt`.
    Second - Run `node ethereum/normalize.js >> watchlists/watch_clean.csv` for csv of hashes.
    Third  - Run `build_watchlist` to create `watch_clean.json`.
    '''
    metadata = {}
    # Requires csv file at WATCH_LOCATION.
    metadata = apply_hashes_to_payload(metadata)
    metadata = ens_claw(metadata)
    with open(f"{app.config['WATCH_LOCATION']}.json", 'w', encoding='utf8') as outfile:
        json.dump(metadata, outfile, indent=4, sort_keys=True, ensure_ascii=False)


def clean_file(file: str = None):
    '''
        Creates a file without new lines, white spaces,
        lower cased, & alphanumerical ordered.

        Run `clean FILE_NAME` in terminal.
    '''
    # import pdb; pdb.set_trace()
    if file == None:
        file = sys.argv[1]

    # Read from uncleaned file.
    with open(f"{app.config['DOMAIN_WATCH_LIST_PATH']}/{file}.txt", 'r') as f:
        app.logger.info(f'Opening file {app.config["DOMAIN_WATCH_LIST_PATH"]}/{file}.txt')
        words = f.readlines()

    clean = []
    for word in words:
        word = word.replace('\n', "").lower()
        clean.append(word)
        if tilde_identifier(word) == True:
            non_tilde_copy = remove_accents(word)
            clean.append(non_tilde_copy.replace('\n', "").lower())

    # Sort & dedup.
    clean.sort()
    clean = list(dict.fromkeys(clean))
    if clean[0] == '':
        clean.pop(0) # Remove whitespace entry
    
    # Produces cleaned human text file.
    f = open(f"{app.config['DOMAIN_WATCH_LIST_PATH']}/{file}_{app.config['CLEAN_LIST']}.txt", 'w')
    app.logger.info(f"Creating {app.config['DOMAIN_WATCH_LIST_PATH']}/{file}_{app.config['CLEAN_LIST']}.txt")
    for word in clean:
        f.write(word.replace(' ', ''))
        f.writelines('\n')
    f.close()


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
