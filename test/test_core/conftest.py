from contextlib import nullcontext as does_not_raise

import pytest

from http_testing._assertion_elements.assertion_data import AssertionData

from .utils import Spec


@pytest.fixture(
    params=[
        Spec(negative=False, expected=pytest.raises(AssertionError)),
        Spec(negative=True, expected=does_not_raise()),
    ],
    ids=["should_not_raise", "should_raise_when_negative"],
)
def should_raise(request):
    return request.param


@pytest.fixture(
    params=[
        Spec(negative=False, expected=does_not_raise()),
        Spec(negative=True, expected=pytest.raises(AssertionError)),
    ],
    ids=["should_not_raise", "should_raise_when_negative"],
)
def should_not_raise(request):
    return request.param


@pytest.fixture
def fake_assertion_data():
    return AssertionData(
        url="http://test/", all_cookies={}, response_status_code=200, response_headers={}, response_text="from test"
    )
