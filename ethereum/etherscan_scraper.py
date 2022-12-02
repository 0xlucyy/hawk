import requests
from pprint import pprint
from bs4 import BeautifulSoup
from scripts.settings import FIXTURE_PATH


from app import (
    app,
    # db
)

# import pdb; pdb.set_trace()

def historical_scraper(payload: dict):
    URL = "https://etherscan.io/token/{contract_address}?a={hash}}"
    html = requests.get(URL.format(contract_address=app.config["ENS_BASE_REGISTRAR_MAINNET"], hash=payload['hash'])).content
    data = BeautifulSoup(html, "html.parser")