import base64
import hashlib
import hmac
import time
import requests
import boto3


def get_api_sign(
    api_path: str, urlencoded_body: str, nonce: str, private_key: str
) -> str:

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
) -> requests.Response:
    nonce_for_first_api_call: str = generate_nonce()
    url_encoded_balance_body: str = f"nonce={nonce_for_first_api_call}"
    balance_api_sign = get_api_sign(
        api_path="/0/private/Balance",
        urlencoded_body=url_encoded_balance_body,
        nonce=nonce_for_first_api_call,
        private_key=private_key,
    )
    balance_response = requests.post(
        url="https://api.kraken.com/0/private/Balance",
        data={"nonce": nonce_for_first_api_call},
        headers={"API-Key": public_key, "API-Sign": balance_api_sign},
    )
    current_balance = balance_response.json()["result"][asset_to_withdraw]

    nonce_for_second_api_call: str = generate_nonce()
    url_encoded_withdraw_body: str = f"nonce={nonce_for_second_api_call}&asset={asset_to_withdraw}&key={withdrawal_address_key}&amount={current_balance}"
    withdraw_api_sign = get_api_sign(
        api_path="/0/private/Withdraw",
        urlencoded_body=url_encoded_withdraw_body,
        nonce=nonce_for_second_api_call,
        private_key=private_key,
    )
    withdraw_response = requests.post(
        url="https://api.kraken.com/0/private/Withdraw",
        data={
            "nonce": nonce_for_second_api_call,
            "asset": asset_to_withdraw,
            "key": withdrawal_address_key,
            "amount": current_balance,
        },
        headers={"API-Key": public_key, "API-Sign": withdraw_api_sign},
    )
    return withdraw_response


def generate_nonce() -> str:
    return str(int(time.time() * 1000))


def get_aws_ssm_securestring_parameter(paramname: str) -> str:
    client = boto3.client("ssm")
    securestring: str = client.get_parameter(Name=paramname, WithDecryption=True)[
        "Parameter"
    ]["Value"]
    return securestring


def lambda_handler(event: dict, context):
    ticker: str = event["ticker"]
    wallet_key: str = get_aws_ssm_securestring_parameter(f"{ticker}-hardwallet")
    private_key: str = get_aws_ssm_securestring_parameter(
        "kraken-private-withdraw-api-key"
    )
    public_key: str = get_aws_ssm_securestring_parameter(
        "kraken-public-withdraw-api-key"
    )

    response: requests.Response = withdraw_crypto_from_kraken(
        ticker, wallet_key, private_key, public_key
    )

    return {"statusCode": 200, "body": response.json()}
