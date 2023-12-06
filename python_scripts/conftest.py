from dataclasses import dataclass
import json
from typing import Union
import pytest
import responses
from urllib.parse import parse_qs


@dataclass
class ResponsesCall:
    request_method: str
    request_url: str
    request_headers: dict
    request_json_body: Union[dict, None] = None
    request_urlencoded_body: Union[str, None] = None


@pytest.fixture
def get_calls_to_responses(mocked_responses):
    def _get_calls_to_responses(method, url) -> list[ResponsesCall]:
        calls = [
            ResponsesCall(
                request_method=method,
                request_url=url,
                request_json_body=json.loads(call.request.body.decode("utf-8"))
                if call.request.headers.get("Content-Type", "") == "application/json"
                else None,
                request_urlencoded_body=parse_qs(call.request.body)
                if call.request.headers.get("Content-Type", "")
                == "application/x-www-form-urlencoded"
                else None,
                request_headers=call.request.headers,
            )
            for call in mocked_responses.calls
            if call.request.method == method and call.request.url == url
        ]

        return calls

    return _get_calls_to_responses


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps


@pytest.fixture(autouse=True)
def setup_default_handlers(mocked_responses):
    mocked_responses.post(
        url="https://api.kraken.com/0/private/AddOrder",
    )
    mocked_responses.post(
        url="https://api.kraken.com/0/private/Withdraw",
    )
