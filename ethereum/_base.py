from web3 import (
    Web3,
    HTTPProvider,
    WebsocketProvider,
    IPCProvider,
    middleware
)
from backend.utils.exceptions import (
    ProviderMissing,
    ProviderOffline
)
from app import (
    app,
    # db
)
# import pdb; pdb.set_trace()


class Web3_Base():
    # load_dotenv() # load environment from .env.

    def __init__(self, name: str = None):
        self.name = name if name else 'session0'
        # self.context = Box()
        # self.load_context()
        # import pdb; pdb.set_trace()
        self.w3 = Web3(self.get_provider())
        # self.w3.geth.txpool.inspect()
        if self.w3.isConnected() == False:
            raise ProviderOffline('Provider is not online.')
    
    def add_middleware(self):
        pass

    def remove_middleware(self):
        pass

    def disconnect(self):
        if self.w3:
            self.w3 = None

    def get_provider(self):
        provider = app.config["MAINNET_PROVIDER"]
        app.logger.info(f'Setting provider {provider}')
        # if app.config['ENV'] == 'live':
        #     provider = app.config["MAINNET_PROVIDER"]
        # else:
        #     provider = app.config["INFURA_PROVIDER"]
        if provider:
            if 'http' in provider:
                return HTTPProvider(provider)
            elif 'ws' in provider:
                return WebsocketProvider(provider)
            elif '.ipc' in provider:
                return IPCProvider(provider)
        raise ProviderMissing('Invalid Provider. Set in settings.py.')

    # def load_context(self):
    #     print('Loading context...')
    #     # Add .env variables to context.
    #     for env_var in os.environ:
    #         if env_var in settings.ENV_ALLOW_LIST:
    #             self.context[env_var] = os.getenv(env_var)

    #     # Add settings.py variables to context.
    #     for key, value in vars(settings).items():
    #         if key in settings.ENV_ALLOW_LIST:
    #             self.context[key] = value
    #     # import pdb; pdb.set_trace()


# test = Web3_Base()
# import pdb; pdb.set_trace()
# print('holding...')