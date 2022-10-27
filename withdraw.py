import time
import requests


def withdraw_crypto_from_kraken(asset_to_withdraw: str, withdrawal_address_key: str):
    nonce: int = int(time.time() * 1000)
    balance_response = requests.post(
        url="https://api.kraken.com/0/private/Balance", data={"nonce": nonce}
    )
    requests.post(
        url="https://api.kraken.com/0/private/Withdraw",
        data={
            "nonce": nonce,
            "asset": asset_to_withdraw,
            "key": withdrawal_address_key,
            "amount": balance_response.json()["result"][asset_to_withdraw],
        },
    )


# TODO:
# - Make sure different nonce is used for the two api calls
# - Use Use amount from first api call to make second api call
# - Add authentication headers to both api calls
