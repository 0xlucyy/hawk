from datetime import datetime
import arrow
from abc import ABC, abstractmethod
from app import (
    app,
    # db
)


NFT_MARKET_SETTINGS = {
    # 'opensea_payload': {
    #     'date_format': 'YYYY-MM-DD HH:mm:ss',
    #     'base_url': app.config["OPENSEA_BASE_URL"],
    #     'api_key': app.config["OPENSEA_API_KEY"],
    #     'use_fail_queue': True
    # },
    'looksrare_payload': {
        'date_format': app.config["DATE_FORMAT"],
        'base_url': app.config["LOOKSRARE_BASE_URL"],
        'api_key': app.config["LOOKSRARE_API_KEY"],
        'use_fail_queue': True
    },
    # 'ensvision_payload': {
    #     'date_format': 'YYYY-MM-DD HH:mm:ss',
    #     'base_url': app.config["ENS_VISION_BASE_URL"],
    #     'api_key': app.config["ENS_VISION_API_KEY"],
    #     'use_fail_queue': True
    # },
    # 'x2y2_payload': {
    #     'date_format': 'YYYY-MM-DD HH:mm:ss',
    #     'base_url': app.config["X2Y2_BASE_URL"],
    #     'api_key': app.config["X2Y2_API_KEY"],
    #     'use_fail_queue': True
    # },
}


class BasePayloadQuerier(ABC):
    @abstractmethod
    def __init__(self, _script_name, _last_run_data):
        env = app.config["ENV"]
        retry_limit = app.config["RETRY_LIMIT"]
        script_name = _script_name
        self.base_url = NFT_MARKET_SETTINGS[script_name]['base_url']
        self.script_settings = NFT_MARKET_SETTINGS[script_name]
        self.start_time = datetime.now()
        self.last_run_data = _last_run_data

    @abstractmethod
    def _get_payload(self):
        pass

    @abstractmethod
    def _get_latest_payloads(self):
        pass

    def _format_start_time(self, timestamp):
        '''
        Convert the given timestamp into a date string so it can be used in
        date filters against the third party sources
        '''
        date_format = self.script_settings['date_format']
        return arrow.get(timestamp).format(date_format)


class LooksRareMarket(BasePayloadQuerier):
    def __init__(self, script_name, start_time, last_run_data):
        super().__init__(script_name, start_time, last_run_data)
        pass

    def _get_payload(self, query):
        '''
        '''
        app.logger.info(f'Querying LooksRare API with: {query}')
        response = self.api.search_cursor(query)
        results = list(response)
        return results