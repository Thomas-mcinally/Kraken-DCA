import pytest
from withdraw import withdraw_crypto_from_kraken


@pytest.mark.parametrize(
    "current_time, expected_nonce, asset_to_withdraw, withdrawal_address_key, current_balance",
    [
        (111.111, "111111", "XXBTZ", "btc_hardwallet", "44.44"),
        (222.222, "222222", "ETH", "eth_hardwallet", "55.55"),
    ],
)
def test_that_calls_to_kraken_balance_and_withdraw_endpoints_are_made_with_values_calculated_from_inputs(
    mocked_responses,
    mocker,
    current_time,
    expected_nonce,
    asset_to_withdraw,
    withdrawal_address_key,
    current_balance,
    get_calls_to_responses,
):
    mocked_responses.post(
        url="https://api.kraken.com/0/private/Balance",
        json={"result": {asset_to_withdraw: current_balance}, "error": []},
    )

    mocker.patch("time.time", return_value=current_time)

    withdraw_crypto_from_kraken(
        asset_to_withdraw=asset_to_withdraw,
        withdrawal_address_key=withdrawal_address_key,
        private_key="kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg==",
        public_key="fake123",
    )

    balance_calls = get_calls_to_responses(
        "POST", "https://api.kraken.com/0/private/Balance"
    )
    assert len(balance_calls) == 1
    assert balance_calls[0].request_urlencoded_body["nonce"] == [expected_nonce]
    withdraw_calls = get_calls_to_responses(
        "POST", "https://api.kraken.com/0/private/Withdraw"
    )
    assert len(withdraw_calls) == 1
    assert withdraw_calls[0].request_urlencoded_body["nonce"] == [expected_nonce]
    assert withdraw_calls[0].request_urlencoded_body["asset"] == [asset_to_withdraw]
    assert withdraw_calls[0].request_urlencoded_body["key"] == [withdrawal_address_key]
    assert withdraw_calls[0].request_urlencoded_body["amount"] == [current_balance]


@pytest.mark.parametrize(
    "time_of_first_api_call,time_of_second_api_call",
    [
        (1.111, 2.222),
        (
            3.333,
            4.444,
        ),
    ],
)
def test_that_calls_to_kraken_balance_and_withdraw_endpoints_are_made_with_different_nonces(
    mocked_responses,
    mocker,
    time_of_first_api_call,
    time_of_second_api_call,
    get_calls_to_responses,
):
    mocked_responses.post(
        url="https://api.kraken.com/0/private/Balance",
        json={"result": {"ETH": "10"}, "error": []},
    )

    mocker.patch(
        "time.time",
        side_effect=(
            time_of_first_api_call,
            time_of_second_api_call,
            time_of_second_api_call,
            time_of_second_api_call,
            time_of_second_api_call,
            time_of_second_api_call,
            time_of_second_api_call,
            time_of_second_api_call,
            time_of_second_api_call,
            time_of_second_api_call,
        ),
    )
    # requests.post calls time function four times, so need to mock time function 10 times
    withdraw_crypto_from_kraken(
        asset_to_withdraw="ETH",
        withdrawal_address_key="eth_wallet",
        private_key="kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg==",
        public_key="fake123",
    )

    balance_calls = get_calls_to_responses(
        "POST", "https://api.kraken.com/0/private/Balance"
    )
    withdrawal_calls = get_calls_to_responses(
        "POST", "https://api.kraken.com/0/private/Withdraw"
    )
    assert len(balance_calls) == 1
    assert len(withdrawal_calls) == 1
    assert (
        balance_calls[0].request_urlencoded_body["nonce"]
        != withdrawal_calls[0].request_urlencoded_body["nonce"]
    )


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
def test_that_call_to_balances_endpoint_is_made_with_required_auth_headers(
    mocked_responses,
    mocker,
    current_time,
    private_key,
    public_key,
    expected_api_Sign,
    get_calls_to_responses,
):
    mocked_responses.post(
        url="https://api.kraken.com/0/private/Balance",
        json={"result": {"BTC": "11"}, "error": []},
    )
    mocker.patch("time.time", return_value=current_time)

    withdraw_crypto_from_kraken(
        asset_to_withdraw="BTC",
        withdrawal_address_key="BTC_wallet",
        private_key=private_key,
        public_key=public_key,
    )

    balance_calls = get_calls_to_responses(
        "POST", "https://api.kraken.com/0/private/Balance"
    )
    assert len(balance_calls) == 1
    assert balance_calls[0].request_headers["API-Key"] == public_key
    assert balance_calls[0].request_headers["API-Sign"] == expected_api_Sign


@pytest.mark.parametrize(
    "public_key, private_key, current_time, asset_to_withdraw, withdrawal_address_key, current_balance, expected_api_sign",
    [
        (
            "fake111",
            "bbbbbb/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg==",
            11.11,
            "BTC",
            "my_BTC_wallet",
            "44.44",
            "JPWHyzVIOvQnbKdUwelvbAD0UxTz9sONLzRDeQhyZUQwEdzYu+qPG2t2dd4A3lziQq6zTOAcD90TjPOz2xf2VA==",
        ),
        (
            "fake222",
            "aaaaaa/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg==",
            22.22,
            "ETH",
            "my_ETH_wallet",
            "55.55",
            "hiN7gz73W52QgY/m382VYLjuhFpLe78MgeQygig9DAze4xIztu8bi0spfDCjZFIkLIoSq2WHHSMMKeSahxLTaA==",
        ),
    ],
)
def test_that_call_to_withdraw_endpoint_is_made_with_required_auth_headers(
    mocker,
    mocked_responses,
    public_key,
    private_key,
    current_time,
    asset_to_withdraw,
    withdrawal_address_key,
    current_balance,
    expected_api_sign,
    get_calls_to_responses,
):
    mocked_responses.post(
        url="https://api.kraken.com/0/private/Balance",
        json={"result": {asset_to_withdraw: current_balance}, "error": []},
    )

    mocker.patch("time.time", return_value=current_time)

    withdraw_crypto_from_kraken(
        asset_to_withdraw=asset_to_withdraw,
        withdrawal_address_key=withdrawal_address_key,
        private_key=private_key,
        public_key=public_key,
    )

    withdrawal_calls = get_calls_to_responses(
        "POST", "https://api.kraken.com/0/private/Withdraw"
    )
    assert len(withdrawal_calls) == 1
    assert withdrawal_calls[0].request_headers["API-Key"] == public_key
    assert withdrawal_calls[0].request_headers["API-Sign"] == expected_api_sign
