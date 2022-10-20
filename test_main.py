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
        ("ETHUSD", "192.125678723", 11, "192.125678", "0.05725418962477259"),
        ("XXBTZUSD", "19200.125678723", 0.5, "19200.125678", "2.6041496206085407e-05"),
    ]
)
def test_calls_to_kraken_endpoints_are_made_with_values_calculated_from_inputs(mocked_responses, ticker, current_market_bid, eur_budget, expected_bid_price, expected_trade_volume):
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


def test_call_to_private_kraken_endpoint_is_made_with_required_headers(mocked_responses):
    mocked_responses.get(
        url="https://api.kraken.com/0/public/Ticker?pair=ETHUSD",
        json={
            "result": {
                "ETHUSD": {
                    "b": [
                        "192.125678723"
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
                "volume": "0.05725418962477259",
                "price": "192.125678",
                "pair": "ETHUSD"
            }),
            matchers.header_matcher({
                "API-Key": "fake123",
                "API-Sign": "fake123" 
            })
        ]
        )
    place_limit_order(ticker="ETHUSD", eur_budget=11)

# list of specs:

# - include nonce in payload (always rising integer. Use unix timestamp)
# - Header called "API-Key" should contain api public key
# - Header called "API-Sign" (generated with your private key, nonce, encoded payload, and URI path)