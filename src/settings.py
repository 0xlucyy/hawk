from web3 import Web3


ENV = 'mainnet'
APP_NAME = 'HAWK'

# Deployments.
AVAH_CONTRACT = Web3.toChecksumAddress("0x47c80DceA83a51A120F8E19e4f3F366c8c393f66")
CREDS_CONTRACT = Web3.toChecksumAddress("0x72A4e5728F993D58646d9d86B19C61b2E7434B1a")
# ENS_CONTRACT = Web3.toChecksumAddress("")
ETH_REGISTRAR_CONTROLLER = Web3.toChecksumAddress("0x283Af0B28c62C092C9727F1Ee09c02CA627EB7F5")

# Transactions.
GAS_INCREASE = .1
MAX_RETRY = 3

# Logging.
LOG_LEVEL = "ERROR" # WARN, INFO, DEBUG, NOTSET
LOG_KEYS = [
    'asctime',
    'timestamp',
    'filename',
    'funcName',
    'lineno',
    'level',
    'message'
]

# Environment variables wanted.
ENV_ALLOW_LIST = [
    # 'ENS_CONTRACT',
    'ETH_REGISTRAR_CONTROLLER',
    'AVAH_CONTRACT',
    'CREDS_CONTRACT',
    'GAS_INCREASE',
    'MAX_RETRY',
    'LOG_LEVEL',
    'LOG_KEYS',
    'APP_NAME',
    'ENV',
    'API_KEY',
    'NORDSTREAM2_PRIV_KEY',
    'FLOWERS_PRIV_KEY',
    'PROVIDER'
]