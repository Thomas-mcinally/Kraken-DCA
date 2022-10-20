from main import place_limit_order
import pytest
import responses
from responses import matchers

@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps

@pytest.mark.parametrize("ticker, current_market_bid, expected_bid_price ",[("ETHUSD", "192.125678123", "192.125678"),("XXBTZUSD", "19200.125678123", "19200.125678")])
def test_call_to_kraken_add_order_endpoint_is_made(mocked_responses, ticker, current_market_bid, expected_bid_price):
    mocked_responses.get(
        url=f"https://api.kraken.com/0/public/Ticker?pair={ticker}",
        json=
            {
  "result": {
    ticker: {
      "a": [
        "string"
      ],
      "b": [
        current_market_bid
      ],
      "c": [
        "string"
      ],
      "v": [
        "string"
      ],
      "p": [
        "string"
      ],
      "t": [
        0
      ],
      "l": [
        "string"
      ],
      "h": [
        "string"
      ],
      "o": "string"
    },
    "pair2": {
      "a": [
        "string"
      ],
      "b": [
        "string"
      ],
      "c": [
        "string"
      ],
      "v": [
        "string"
      ],
      "p": [
        "string"
      ],
      "t": [
        0
      ],
      "l": [
        "string"
      ],
      "h": [
        "string"
      ],
      "o": "string"
    }
  },
  "error": [
    "EGeneral:Invalid arguments"
  ]
}
        
    )
    mocked_responses.post(
        url = "https://api.kraken.com/0/private/AddOrder",
        match = [
            matchers.json_params_matcher({
                "ordertype": "limit",
                "type": "buy",
                "volume": "0.002",
                "price": expected_bid_price,
                "pair": ticker
            })
        ]
        )
    
    place_limit_order(ticker=ticker, eur_budget=11)




# list of specs:
# - include nonce in payload (always rising integer. Use unix timestamp)
# - Header called "API-Key" should contain api keyname
# - Header called "API-Sign" (generated with your private key, nonce, encoded payload, and URI path)
# - pass required body params

# - Look up and change pair body parameter value later on