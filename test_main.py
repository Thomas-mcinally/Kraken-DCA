from main import place_limit_order
import pytest
import responses
from responses import matchers

@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps

@pytest.mark.parametrize(
    "ticker, current_market_bid, eur_budget, expected_bid_price, expected_trade_volume",
    [
        ("ETHUSD", "192.125678123", 11, "192.125678", "0.05725418962477259"),
        ("XXBTZUSD", "19200.125678123", 0.5, "19200.125678", "2.6041496206085407e-05"),
    ]
)
def test_call_to_kraken_add_order_endpoint_is_made(mocked_responses, ticker, current_market_bid, eur_budget, expected_bid_price, expected_trade_volume):
    mocked_responses.get(
        url=f"https://api.kraken.com/0/public/Ticker?pair={ticker}",
        json={
            "result": {
                ticker: {
                    "b": [
                        current_market_bid
                    ],
                }
            }
        }
    )
    mocked_responses.post(
        url = "https://api.kraken.com/0/private/AddOrder",
        match = [
            matchers.json_params_matcher({
                "ordertype": "limit",
                "type": "buy",
                "volume": expected_trade_volume,
                "price": expected_bid_price,
                "pair": ticker
            })
        ]
        )
    
    place_limit_order(ticker=ticker, eur_budget=eur_budget)




# list of specs:
# - include nonce in payload (always rising integer. Use unix timestamp)
# - Header called "API-Key" should contain api keyname
# - Header called "API-Sign" (generated with your private key, nonce, encoded payload, and URI path)
# - pass required body params

# - Look up and change pair body parameter value later on