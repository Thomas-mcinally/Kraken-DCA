import pytest
import responses
from responses import matchers
from withdraw import withdraw_crypto_from_kraken


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.mark.parametrize(
    "current_time, expected_nonce, asset_to_withdraw, withdrawal_address_key, current_balance",
    [
        (111.111, "111111", "XXBTZ", "btc_hardwallet", "44.44"),
        (222.222, "222222", "ETH", "eth_hardwallet", "55.55"),
    ],
)
def test_calls_to_kraken_balance_and_withdraw_endpoints_are_made(
    mocked_responses,
    mocker,
    current_time,
    expected_nonce,
    asset_to_withdraw,
    withdrawal_address_key,
    current_balance,
):
    mocked_responses.post(
        url="https://api.kraken.com/0/private/Balance",
        match=[matchers.urlencoded_params_matcher({"nonce": expected_nonce})],
        json={"result": {asset_to_withdraw: current_balance}, "error": []},
    )

    mocked_responses.post(
        url="https://api.kraken.com/0/private/Withdraw",
        match=[
            matchers.urlencoded_params_matcher(
                {
                    "nonce": expected_nonce,
                    "asset": asset_to_withdraw,
                    "key": withdrawal_address_key,
                    "amount": current_balance,
                }
            )
        ],
    )
    mocker.patch("time.time", return_value=current_time)

    withdraw_crypto_from_kraken(
        asset_to_withdraw=asset_to_withdraw,
        withdrawal_address_key=withdrawal_address_key,
        private_key="kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg==",
        public_key="fake123",
    )


def test_calls_to_kraken_balance_and_withdraw_endpoints_are_made_with_different_nonces(
    mocked_responses,
):
    # FIGURE OUT HOW TO TEST THIS LATER, CURRENTLY USING SAME NONCE FOR BOTH CALLS
    pass


@pytest.mark.parametrize(
    "current_time, private_key, public_key, expected_api_Sign",
    [
        (
            88.88,
            "kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg==",
            "fake333",
            "bR2T+AbzdsepTMgJXnA8TInMDmqGvy6P+LmXdwmfjrdKj9b6HsJcAoNO4AZj4vn+NNZ72JITjgCTt1jhZonTxg==",
        ),
        (
            99.99,
            "111111/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg==",
            "fake444",
            "+xvi2JFr0s1f34mfyjXDYDj3YyXj3ZSvdIrGiCZolqwEes3zlGfhz+zKVlZvunalMtiE/6QNrxHkW73UGjM7oQ==",
        ),
    ],
)
def test_call_to_balances_endpoint_is_made_with_required_auth_headers(
    mocked_responses, mocker, current_time, private_key, public_key, expected_api_Sign
):
    mocked_responses.post(
        url="https://api.kraken.com/0/private/Balance",
        match=[
            matchers.header_matcher(
                {"API-Key": public_key, "API-Sign": expected_api_Sign}
            )
        ],
        json={"result": {"BTC": "11"}, "error": []},
    )
    mocked_responses.post(
        url="https://api.kraken.com/0/private/Withdraw",
    )
    mocker.patch("time.time", return_value=current_time)

    withdraw_crypto_from_kraken(
        asset_to_withdraw="BTC",
        withdrawal_address_key="BTC_wallet",
        private_key=private_key,
        public_key=public_key,
    )


@pytest.mark.parametrize(
    "public_key",
    [("fake111"), ("fake222")],
)
def test_call_to_withdraw_endpoint_is_made_with_required_auth_headers(
    mocked_responses, public_key
):
    mocked_responses.post(
        url="https://api.kraken.com/0/private/Balance",
        json={"result": {"BTC": "11"}, "error": []},
    )
    mocked_responses.post(
        url="https://api.kraken.com/0/private/Withdraw",
        match=[matchers.header_matcher({"API-Key": public_key})],
    )
    withdraw_crypto_from_kraken(
        asset_to_withdraw="BTC",
        withdrawal_address_key="BTC_wallet",
        private_key="kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg==",
        public_key=public_key,
    )
