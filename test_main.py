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
    
    place_limit_order(ticker=ticker, eur_budget=eur_budget, private_key="123")


def test_call_to_private_kraken_endpoint_is_made_with_required_headers(mocked_responses, mocker):
    mocked_responses.get(
        url="https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
        json={
            "result": {
                "XBTUSD": {
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
                "pair": "XBTUSD"
            }),
            matchers.header_matcher({
                "API-Key": "fake123",
                "API-Sign": "4/dpxb3iT4tp/ZCVEwSnEsLxx0bqyhLpdfOpc6fn7OR8+UClSV5n9E6aSS8MPtnRfp32bAb0nmbRn6H8ndwLUQ==" 
            })
        ]
        )

    mocker.patch("time.time", return_value=1616492376.594)

    place_limit_order(ticker="XBTUSD", eur_budget=11, private_key="kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg==")


# list of specs:
# Enforce dynamic generation of digital signature. 
    #  got correct formula. Now just need to parametrize all the components that go into making it, and the final signature resulting from these
# - include nonce in payload (always rising integer. Use unix timestamp)
# - Header called "API-Key" should contain api public key
