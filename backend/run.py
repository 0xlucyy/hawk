import requests

def main():
    print('hello from src/main.py')

    import requests

    url = "https://api.opensea.io/api/v1/asset/0xbea8123277142de42571f1fac045225a1d347977/43/?include_orders=true"
    headers = {
        "accept": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    print(response.text)