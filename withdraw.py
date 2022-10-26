import time
import requests


def withdraw_crypto_from_kraken(asset_to_withdraw: str, withdrawal_address_key: str):
    nonce: int = int(time.time() * 1000)
    requests.post(url="https://api.kraken.com/0/private/Balance", data={"nonce": nonce})
    requests.post(
        url="https://api.kraken.com/0/private/Withdraw",
        data={
            "nonce": nonce,
            "asset": asset_to_withdraw,
            "key": withdrawal_address_key,
            "amount": 0.123
        },
    )
