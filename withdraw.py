import requests


def withdraw_crypto_from_kraken():
    requests.post(url='https://api.kraken.com/0/private/Balance')