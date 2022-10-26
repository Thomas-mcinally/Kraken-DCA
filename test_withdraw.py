import pytest
import responses
from responses import matchers
from withdraw import withdraw_crypto_from_kraken

@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_call_to_kraken_balance_endpoint_is_made(mocked_responses):
    mocked_responses.post(
        url='https://api.kraken.com/0/private/Balance',
        match=[
            matchers.urlencoded_params_matcher(
                {
                    'nonce': '123'
                }
            )
        ]
    )
    withdraw_crypto_from_kraken()