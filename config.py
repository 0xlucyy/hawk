import os
import logging
from web3 import Web3
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# import pdb; pdb.set_trace()

'''
    Domain can be held by someone
    Domain can be registered by anyone
    domain can be in grace
    domain can be in auction
'''
class _Base(object):
    APP_NAME = 'hawk'
    GAS_INCREASE = .1
    ENV = os.environ.get("ENV")
    DATE_FORMAT = os.environ.get("DATE_FORMAT")
    API_URI = os.environ.get("API_URI")
    RETRY_LIMIT = os.environ.get("RETRY_LIMIT")
    PRIV_KEY_ONE = os.environ.get("PRIV_KEY_ONE")
    
    # DB
    MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DB = os.environ.get("MYSQL_DB")

    # Ethereum network connections.
    MAINNET_PROVIDER = os.environ.get("MAINNET_PROVIDER")
    GOERLI_PROVIDER = os.environ.get("GOERLI_PROVIDER")
    
    # GraphQL
    GRAPHQL_API_KEY = os.environ.get("GRAPHQL_API_KEY")
    # GRAPHQL_ENS_URL = f"https://gateway.thegraph.com/api/{GRAPHQL_API_KEY}/subgraphs/id/EjtE3sBkYYAwr45BASiFp8cSZEvd1VHTzzYFvJwQUuJx"
    GRAPHQL_ENS_URL = 'https://api.thegraph.com/subgraphs/name/ensdomains/ens'

    # Etherscan APIs
    ETHERSCAN_TOKEN = os.environ.get("ETHERSCAN_TOKEN")
    ETHERSCAN_TX_SCAN = 'https://api.etherscan.io/api?module=account&action=txlistinternal&txhash=0x53bedcfc03842aabf0a910a173b3632f05dcb11985f4dee20f35553694b9015d&apikey={ETHERSCAN_TOKEN}'
    ETHRSCAN_GET_GAS = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={API_TOKEN}'

    # Clean watch list settings.
    SPANISH_TILDES = ['á', 'é', 'í', 'ó', 'ú', 'ü', 'ñ']
    CLEAN_FILE = 'clean'
    DOMAIN_WATCH_FOLDER = 'watchlists'
    WATCH_LOCATION = f'{DOMAIN_WATCH_FOLDER}/watch_clean'
    DATETIME_STR_FORMAT = '%Y-%m-%d %H:%M:%S'
    ENS_GRACE_PERIOD = 90 # days
    ENS_AUCTION_PERIOD = 21 # days

    # Domain statuses
    DOMAIN_STATUS_FREE = 'FREE'
    DOMAIN_STATUS_IN_GRACE = 'IN_GRACE'
    DOMAIN_STATUS_IN_AUCTION = 'IN_AUCTION'
    DOMAIN_STATUS_HODLING = 'BEING_HELD'

    # ENS length costs in USD
    THREE_LETTER = 640 # six hundred & forty USD per year.
    FOUR_LETTER = 160 # one hundreds & sixty USD per year.
    MORE_THEN_FOUR_LETTERS = 5 # Five dollars USD per year.

    # ENS contract deployments.
    ENS_ETH_REGISTRAR_CONTROLLER_MAINNET = Web3.toChecksumAddress("0x283Af0B28c62C092C9727F1Ee09c02CA627EB7F5")
    ENS_BASE_REGISTRAR_MAINNET = Web3.toChecksumAddress("0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85")
    ENS_REVERSE_RECORDS_MAINNET = Web3.toChecksumAddress("0x3671aE578E63FdF66ad4F3E12CC0c0d71Ac7510C")

    # ENS Metadata service.
    ENS_META_SERVICE = "https://metadata.ens.domains/mainnet/{eth_network}/{domain_hash}/"

    # Logging.
    LOGGING_DEBUG_LOCATION = os.path.dirname(__file__) + '/debug.log'
    # LOGGING_FORMAT = '[%(levelname)s] - %(name)s - %(asctime)s - %(funcName)s::%(lineno)d - %(message)s'
    LOGGING_FORMAT = '%(asctime)s %(levelname)-6s [%(filename)s::%(funcName)s():%(lineno)d] %(message)s'
    LOGGING_LEVEL =  logging.INFO
    SQLALCHEMY_ECHO = False


class Config(_Base):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    # print(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = False

class TestConfiguration(_Base):
    DEBUG = True
    TESTING = True
    DATABASE = f"{os.environ.get('MYSQL_DB')}.db"
    DATABASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), DATABASE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
    # sqlite:////Users/ancientevil/0x/hawk/hawk.db
    # print(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    HASH_ROUNDS = 1
    SQLALCHEMY_TRACK_MODIFICATIONS = True

def set_logger():
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': _Base.LOGGING_FORMAT
            }
        },
        'handlers': {
            'default': { 
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
                'formatter': 'default',
                'level'    : 'INFO'
            },
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default',
                'level'    : 'INFO'
            },
            'DEBUG_FILE': {
                'class' : 'logging.FileHandler',
                'formatter': 'default',
                'filename' : _Base.LOGGING_DEBUG_LOCATION,
                'level'    : 'DEBUG'
            }
        },
        'root': {
            'level': _Base.LOGGING_LEVEL,
            # 'handlers': ['wsgi']
            'handlers': ['default', 'DEBUG_FILE']
        }
    }
    return logging_config
