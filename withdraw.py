import time
import requests


def withdraw_crypto_from_kraken():
    nonce: int = int(time.time() * 1000)
    requests.post(
        url='https://api.kraken.com/0/private/Balance',
        data={'nonce':nonce}
    )