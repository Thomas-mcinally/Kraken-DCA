import pytest
import responses
from responses import matchers
from withdraw import withdraw_crypto_from_kraken

@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.mark.parametrize(
    "current_time, expected_nonce",
    [
        (111.111, '111111'),
        (222.222, '222222')
    ],
)
def test_call_to_kraken_balance_endpoint_is_made(mocked_responses, mocker, current_time, expected_nonce):
    mocked_responses.post(
        url='https://api.kraken.com/0/private/Balance',
        match=[
            matchers.urlencoded_params_matcher(
                {
                    'nonce': expected_nonce
                }
            )
        ],
        json={
            "result": {
                "ZUSD": "2970172.7962"
            },
            "error": []
        }
    )
    mocker.patch("time.time", return_value=current_time)

    withdraw_crypto_from_kraken()