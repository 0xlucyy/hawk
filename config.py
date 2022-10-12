import os
import logging
from web3 import Web3
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# import pdb; pdb.set_trace()

class _Base(object):
    APP_NAME = 'hawk'
    GAS_INCREASE = .1
    ENV = os.environ.get("ENV")
    DATE_FORMAT = os.environ.get("DATE_FORMAT")
    API_URI = os.environ.get("API_URI")
    RETRY_LIMIT = os.environ.get("RETRY_LIMIT")
    NORDSTREAM2_PRIV_KEY = os.environ.get("NORDSTREAM2_PRIV_KEY")
    
    # DB
    MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DB = os.environ.get("MYSQL_DB")

    # Ethereum network connections.
    MAINNET_PROVIDER = os.environ.get("MAINNET_PROVIDER")
    ROPSTEN_PROVIDER = os.environ.get("ROPSTEN_PROVIDER")
    INFURA_PROVIDER = os.environ.get("INFURA_PROVIDER")

    # Clean watch list settings.
    SPANISH_TILDES = ['á', 'é', 'í', 'ó', 'ú', 'ü', 'ñ']
    CLEAN_FILE = 'clean'
    DOMAIN_WATCH_FOLDER = 'watchlists'
    WATCH_LOCATION = f'{DOMAIN_WATCH_FOLDER}/watch_clean'
    DATETIME_STR_FORMAT = '%Y-%m-%d %H:%M:%S'
    # ENS Basic Registrar contract ownerOf reverts
    # when domain is in auction/grace.
    ENS_GRACE_AUCTION = 'Domain in grace or auction.'
    # Order model formatter
    ORDERS = ''

    # Deployments.
    ETH_REGISTRAR_CONTROLLER_MAINNET = Web3.toChecksumAddress("0x283Af0B28c62C092C9727F1Ee09c02CA627EB7F5")
    ENS_BASE_REGISTRAR_MAINNET = Web3.toChecksumAddress("0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85")
    DYSTOPUNKS_V2_MAINNET = Web3.toChecksumAddress("0xbEA8123277142dE42571f1fAc045225a1D347977")

    LOOKSRARE_BASE_URL = os.environ.get("LOOKSRARE_BASE_URL")
    LOOKSRARE_API_KEY = os.environ.get("LOOKSRARE_API_KEY")
    LOOKSRARE_GET_EVENTS = os.environ.get("LOOKSRARE_GET_EVENTS")
    ENSVISION_INFO = "https://www.ens.vision/name/{domain}"

    # Logging.
    LOG_KEYS = [
        'asctime',
        'timestamp',
        'filename',
        'funcName',
        'lineno',
        'level',
        'message'
    ]
    LOGGING_DEBUG_LOCATION = os.path.dirname(__file__) + '/DEBUG.log'
    LOGGING_FORMAT = '[%(levelname)s] - %(name)s - %(asctime)s - %(funcName)s::%(lineno)d - %(message)s'
    LOGGING_LEVEL = logging.INFO
    SQLALCHEMY_ECHO = False


class Config(_Base):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    print(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = False

class TestConfiguration(_Base):
    DEBUG = True
    TESTING = True
    DATABASE = f"{os.environ.get('MYSQL_DB')}.db"
    DATABASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), DATABASE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
    # sqlite:////Users/ancientevil/0x/hawk/hawk.db
    print(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    HASH_ROUNDS = 1
    SQLALCHEMY_TRACK_MODIFICATIONS = True

def set_logger():
    logging_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': _Base.LOGGING_FORMAT
            }
        },
        'handlers': {
            'default': { 
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
                'formatter': 'default'
            },            
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
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