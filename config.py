import os
import logging
from web3 import Web3
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# import pdb; pdb.set_trace()

class _Base(object):
    APP_NAME = 'HAWK'
    ENV = os.environ.get("ENV")
    API_URI = os.environ.get("API_URI")

    # Deployments.
    AVAH_CONTRACT = Web3.toChecksumAddress("0x47c80DceA83a51A120F8E19e4f3F366c8c393f66")
    CREDS_CONTRACT = Web3.toChecksumAddress("0x72A4e5728F993D58646d9d86B19C61b2E7434B1a")
    ETH_REGISTRAR_CONTROLLER = Web3.toChecksumAddress("0x283Af0B28c62C092C9727F1Ee09c02CA627EB7F5")

    # Transactions.
    GAS_INCREASE = .1
    MAX_RETRY = 3

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
    LOGGING_LOCATION = os.path.dirname(__file__) + '/app.log'
    LOGGING_FORMAT = '%(levelname)s - %(name)s - %(asctime)s - %(funcName)s::%(lineno)d - %(message)s'
    LOGGING_LEVEL = logging.DEBUG

    SQLALCHEMY_ECHO = True


class Config(_Base):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    print(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = False

class TestConfiguration(_Base):
    # import pdb; pdb.set_trace()
    DEBUG = True
    TESTING = True
    DATABASE = 'ENS.db'
    DATABASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), DATABASE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
    print(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    HASH_ROUNDS = 1
    SQLALCHEMY_TRACK_MODIFICATIONS = True

def logger(app):
    handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], maxBytes=10000, backupCount=0)
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    handler.setLevel(app.config['LOGGING_LEVEL'])
    app.logger.setLevel(app.config['LOGGING_LEVEL'])
    app.logger.addHandler(handler)
