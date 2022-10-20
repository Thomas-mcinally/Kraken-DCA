from main import place_limit_order
import pytest
import responses

@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps

def test_call_to_kraken_add_order_endpoint_is_made(mocked_responses):
    mocked_responses.post("https://api.kraken.com/0/private/AddOrder")
    
    place_limit_order(ticker="ETH-USD", amount_to_purchase=0.002, leverage=0.0, limit_price=129.1)