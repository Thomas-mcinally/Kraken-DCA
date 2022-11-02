import base64
import hashlib
import hmac
import math
import time
import requests
import boto3


def place_limit_order_on_kraken(
    trading_pair: str, budget: float, private_key: str, public_key: str
) -> requests.Response:
    bid_price: str = get_bid_price(trading_pair)
    volume: str = get_trade_volume(budget, bid_price)
    nonce: str = str(int(time.time() * 1000))
    url_encoded_body: str = f"nonce={nonce}&ordertype=limit&pair={trading_pair}&price={bid_price}&type=buy&volume={volume}"
    api_sign: str = get_api_sign(
        api_path="/0/private/AddOrder",
        urlencoded_body=url_encoded_body,
        nonce=nonce,
        private_key=private_key,
    )

    response: requests.Response = requests.post(
        url="https://api.kraken.com/0/private/AddOrder",
        data={
            "nonce": nonce,
            "ordertype": "limit",
            "pair": trading_pair,
            "price": bid_price,
            "type": "buy",
            "volume": volume,
        },
        headers={"API-Key": public_key, "API-Sign": api_sign},
    )
    return response


def round_down(n: float, decimals: int) -> float:
    multiplier: int = 10**decimals
    return math.floor(n * multiplier) / multiplier


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


def get_bid_price(trading_pair: str) -> str:
    market_data: dict = requests.get(
        url=f"https://api.kraken.com/0/public/Ticker?pair={trading_pair}"
    ).json()
    top_market_bid: float = float(market_data["result"][trading_pair]["b"][0])
    my_bid_price: str = str(round_down(top_market_bid, decimals=6))
    return my_bid_price


def get_trade_volume(budget: float, bid_price: str) -> str:
    return str(budget / float(bid_price))


def get_aws_ssm_securestring_parameter(paramname: str) -> str:
    client = boto3.client("ssm")
    securestring: str = client.get_parameter(Name=paramname, WithDecryption=True)[
        "Parameter"
    ]["Value"]
    return securestring


def lambda_handler(event, context) -> dict:
    budget: float = float(
        get_aws_ssm_securestring_parameter("kraken-dca-BTC-daily-purchase-amount")
    )
    private_key: str = get_aws_ssm_securestring_parameter("kraken-private-api-key")
    public_key: str = get_aws_ssm_securestring_parameter("kraken-public-api-key")

    response: requests.Response = place_limit_order_on_kraken(
        trading_pair="XXBTZEUR",
        budget=budget,
        private_key=private_key,
        public_key=public_key,
    )

    return {"statusCode": 200, "body": response.json()}
