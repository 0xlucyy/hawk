from datetime import datetime
import arrow
from box import Box
from abc import ABC, abstractmethod
from backend.utils.utils import stringify
from app import (
    app,
    # db
)
# import pdb; pdb.set_trace()


MARKET_SETTINGS = {
    # 'opensea_payload': {
    #     'date_format': 'YYYY-MM-DD HH:mm:ss',
    #     'base_url': app.config["OPENSEA_BASE_URL"],
    #     'api_key': app.config["OPENSEA_API_KEY"],
    #     'use_fail_queue': True
    # },
    'looksrare': {
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
    def __init__(self, _script, _last_run):
        self.script_name = _script
        self.last_run_data = _last_run
        self.start_time = datetime.now()
        self.settings = Box()
        self.settings = self.settings.from_json(stringify(MARKET_SETTINGS[self.script_name]))

    @abstractmethod
    def _get_payload(self):
        pass

    @abstractmethod
    def _get_latest_payloads(self):
        pass

    def _format_start_time(self, timestamp):
        '''
        Convert timestamp into date string so it can be used in
        date filters on third partys.
        '''
        _date_format = self.script_settings.date_format
        return arrow.get(timestamp).format(_date_format)


class LooksRareMarket(BasePayloadQuerier):
    def __init__(self, _script, _last_run):
        super().__init__(_script, _last_run)
        # import pdb; pdb.set_trace()
        print('holding...')
        pass

    def _get_payload(self, query):
        '''
        '''
        app.logger.info(f'Querying LooksRare API with: {query}')
        response = self.settings.base_url # MAKE CALL
        results = list(response)
        return results

    def _get_latest_payloads(self):
        print('implement')

# test = LooksRareMarket('looksrare', 1111)
# test._get_latest_payloads()