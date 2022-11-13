from contextlib import nullcontext
from unittest import mock

import pytest
from httpx import Client, Response

from .utils import Spec


@pytest.fixture(
    params=[
        Spec(negative=False, expected=pytest.raises(AssertionError)),
        Spec(negative=True, expected=nullcontext()),
    ],
    ids=["should_not_raise", "should_raise_when_negative"],
)
def should_raise(request):
    return request.param


@pytest.fixture(
    params=[
        Spec(negative=False, expected=nullcontext()),
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
    return mock.MagicMock(spec=Response, auto_spec=True)
