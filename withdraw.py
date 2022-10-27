import base64
import hashlib
import hmac
import time
import requests


def get_api_sign(api_path, urlencoded_body, nonce, private_key):

    api_sha256: hashlib._Hash = hashlib.sha256(
        nonce.encode() + urlencoded_body.encode()
    )
    api_hmac: hmac.HMAC = hmac.new(
        base64.b64decode(private_key),
        api_path.encode() + api_sha256.digest(),
        hashlib.sha512,
    )
    api_signature: bytes = base64.b64encode(api_hmac.digest())
    api_signature_decoded: str = api_signature.decode()
    return api_signature_decoded


def withdraw_crypto_from_kraken(
    asset_to_withdraw: str,
    withdrawal_address_key: str,
    private_key: str,
    public_key: str,
):
    nonce: int = int(time.time() * 1000)

    url_encoded_balance_body: str = f"nonce={nonce}"
    balance_api_sign = get_api_sign(
        api_path="/0/private/Balance",
        urlencoded_body=url_encoded_balance_body,
        nonce=str(nonce),
        private_key=private_key,
    )
    balance_response = requests.post(
        url="https://api.kraken.com/0/private/Balance",
        data={"nonce": nonce},
        headers={"API-Key": public_key, "API-Sign": balance_api_sign},
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
# - Add authentication headers to both api calls
