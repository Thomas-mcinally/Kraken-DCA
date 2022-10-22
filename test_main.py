from btc_dca_script import place_limit_order
import pytest
import responses
from responses import matchers

@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps

@pytest.mark.parametrize(
    "trading_pair, current_market_bid, budget, current_time, expected_nonce, expected_bid_price, expected_trade_volume",
    [
        ("ETHUSD", "192.125678723", 11, 222.222, "222222", "192.125678", "0.05725418962477259"),
        ("XXBTZUSD", "19200.125678723", 0.5, 111.111, "111111", "19200.125678", "2.6041496206085407e-05"),
    ]
)
def test_calls_to_kraken_endpoints_are_made_with_values_calculated_from_inputs(mocked_responses, mocker, trading_pair, current_market_bid, budget, current_time, expected_nonce, expected_bid_price, expected_trade_volume):
    mocked_responses.get(
        url=f"https://api.kraken.com/0/public/Ticker?pair={trading_pair}",
        json={
            "result": {
                trading_pair: {
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
            matchers.urlencoded_params_matcher({
                "nonce": expected_nonce,
                "ordertype": "limit",
                "pair": trading_pair,
                "price": expected_bid_price,
                "type": "buy",
                "volume": expected_trade_volume
            })
        ]
        )
    mocker.patch("time.time", return_value=current_time)
    place_limit_order(trading_pair=trading_pair, budget=budget, private_key="kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg==", public_key="111")



@pytest.mark.parametrize(
    "trading_pair, current_market_bid, budget, current_time, private_key, expected_api_Sign, public_key",
    [
        ("ETHUSD", "192.125678723", 11, 1616492376.594, "kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg==", "l8th/OmRDGpwfHAoOCIuZF+c9X37krK1KELhRUoEcQU2Si3gHtCY/mPeIgw7saRe1fREa6vfMDIUSEs6ov+fEQ==", "fake111"),
        ("XXBTZUSD", "19200.125678723", 0.5, 1111111111.594, "111111/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg==", "HxAjpPcHJZDU3dRdaBtZ312pqV2pD3zaeglYxpmeEjgVUUlJ62m8QQbjjmyVm2X+gc491tCdwKAIW1ACJJxvGA==", "fake222"),
    ]
)
def test_call_to_private_kraken_endpoint_is_made_with_required_headers_and_nonce_is_included_in_body(mocked_responses, mocker, trading_pair, current_market_bid, budget, current_time, private_key, expected_api_Sign, public_key):
    mocked_responses.get(
        url=f"https://api.kraken.com/0/public/Ticker?pair={trading_pair}",
        json={
            "result": {
                trading_pair: {
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
            matchers.header_matcher({
                "API-Key": public_key,
                "API-Sign": expected_api_Sign 
            })
        ]
        )

    mocker.patch("time.time", return_value=current_time)

    place_limit_order(trading_pair=trading_pair, budget=budget, private_key=private_key, public_key=public_key)
