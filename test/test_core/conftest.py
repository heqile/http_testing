from contextlib import nullcontext as does_not_raise
from unittest import mock

import pytest
from httpx import Client, Response

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
def mock_client():
    return mock.MagicMock(spec=Client, auto_spec=True)


@pytest.fixture
def mock_response():
    mock_client = mock.MagicMock(spec=Response, auto_spec=True)
    mock_client.headers = {}
    mock_client.status_code = 200
    return mock_client
