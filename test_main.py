from curses import keyname
from main import place_limit_order
import pytest
import responses
from responses import matchers

@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps

def test_call_to_kraken_add_order_endpoint_is_made(mocked_responses):
    mocked_responses.post(
        url = "https://api.kraken.com/0/private/AddOrder",
        match = [
            matchers.json_params_matcher({
                "ordertype": "limit",
                "type": "buy",
                "volume": 0.002,
                "pair": "ETH-USD"
            })
        ]
        )
    
    place_limit_order(ticker="ETH-USD", amount_to_purchase=0.002, leverage=0.0, limit_price=129.1)




# list of specs:
# - include nonce in payload (always rising integer. Use unix timestamp)
# - Header called "API-Key" should contain api keyname
# - Header called "API-Sign" (generated with your private key, nonce, encoded payload, and URI path)
# - pass required body params

# - Look up and change pair body parameter value later on