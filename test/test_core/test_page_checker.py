from contextlib import AbstractContextManager, nullcontext
from typing import Any, Dict, Sequence

import pytest
from httpx import Client
from respx import MockRouter, SetCookie

from http_testing import Assertions, Cookie, NegativeAssertions, PageChecker, Regex, Text

pytestmark = [pytest.mark.respx(base_url="http://localhost")]


@pytest.fixture
def http_client():
    with Client() as client:
        yield client


@pytest.mark.parametrize(
    ["response_status_code", "expected_status_code", "is_negative", "should_raise"],
    [
        pytest.param(200, 200, False, False, id="should_not_raise_if_should_find_is_ok"),
        pytest.param(200, 400, False, True, id="should_raise_if_should_find_is_ko"),
        pytest.param(200, 400, True, False, id="should_not_raise_if_should_not_find_is_ok"),
        pytest.param(200, 200, True, True, id="should_raise_if_should_not_find_is_ko"),
    ],
)
def test_page_checker_assert_status(
    http_client: Client,
    response_status_code: int,
    expected_status_code: int,
    is_negative: bool,
    should_raise: bool,
    respx_mock: MockRouter,
):
    respx_mock.get("/test_page.html").respond(status_code=response_status_code)
    check = PageChecker(base_url="http://localhost", http_client=http_client)
    kwargs: Dict[str, Any] = {}
    if not is_negative:
        kwargs["should_find"] = Assertions(status_code=expected_status_code)
    else:
        kwargs["should_not_find"] = NegativeAssertions(status_code=expected_status_code)

    cm: AbstractContextManager
    if should_raise:
        cm = pytest.raises(AssertionError)
    else:
        cm = nullcontext()
    with cm:
        check(path="/test_page.html", title="from_unit_test", **kwargs)


@pytest.mark.parametrize(
    ["response_headers", "expected_headers", "is_negative", "should_raise"],
    [
        pytest.param(
            {"foo": "bar"},
            {"foo": "bar"},
            False,
            False,
            id="should_not_raise_if_should_find_is_ok_with_str_value",
        ),
        pytest.param(
            {"foo": "bar"},
            {"foo": Regex("b.*")},
            False,
            False,
            id="should_not_raise_if_should_find_is_ok_with_regex_validator",
        ),
        pytest.param(
            {"foo": "bar"},
            {"foo": Text("bar")},
            False,
            False,
            id="should_not_raise_if_should_find_is_ok_with_text_validator",
        ),
        pytest.param(
            {"foo": "bar"},
            {"foo": "ooops"},
            False,
            True,
            id="should_raise_if_should_find_is_ko_with_str_value",
        ),
        pytest.param(
            {"foo": "bar"},
            {"foo": Regex("o.*")},
            False,
            True,
            id="should_raise_if_should_find_is_ko_with_regex_value",
        ),
        pytest.param(
            {"foo": "bar"},
            {"foo": Text("ooops")},
            False,
            True,
            id="should_raise_if_should_find_is_ko_with_text_value",
        ),
        pytest.param(
            {"foo": "bar"},
            {"foo": "ooops"},
            True,
            False,
            id="should_not_raise_if_should_not_find_is_ok_with_str_value",
        ),
        pytest.param(
            {"foo": "bar"},
            {"foo": Regex("o.*")},
            True,
            False,
            id="should_not_raise_if_should_not_find_is_ok_with_regex_value",
        ),
        pytest.param(
            {"foo": "bar"},
            {"foo": Text("ooops")},
            True,
            False,
            id="should_not_raise_if_should_not_find_is_ok_with_text_value",
        ),
        pytest.param(
            {"foo": "bar"},
            {"foo": "bar"},
            True,
            True,
            id="should_raise_if_should_not_find_is_ko_with_str_value",
        ),
        pytest.param(
            {"foo": "bar"},
            {"foo": Regex("b.*")},
            True,
            True,
            id="should_raise_if_should_not_find_is_ko_with_regex_value",
        ),
        pytest.param(
            {"foo": "bar"},
            {"foo": Text("bar")},
            True,
            True,
            id="should_raise_if_should_not_find_is_ko_with_text_value",
        ),
    ],
)
def test_page_checker_assert_headers(
    http_client: Client,
    response_headers: Dict[str, str],
    expected_headers: Dict[str, Any],
    is_negative: bool,
    should_raise: bool,
    respx_mock: MockRouter,
):
    respx_mock.get("/test_page.html").respond(headers=response_headers)
    check = PageChecker(base_url="http://localhost", http_client=http_client)
    kwargs: Dict[str, Any] = {}
    if not is_negative:
        kwargs["should_find"] = Assertions(headers=expected_headers)
    else:
        kwargs["should_not_find"] = NegativeAssertions(headers=expected_headers)

    cm: AbstractContextManager
    if should_raise:
        cm = pytest.raises(AssertionError)
    else:
        cm = nullcontext()
    with cm:
        check(path="/test_page.html", title="from_unit_test", **kwargs)


@pytest.mark.parametrize(
    ["response_cookies", "expected_cookies", "is_negative", "should_raise"],
    [
        pytest.param(
            {"cookie_one": "cool"},
            [Cookie(name="cookie_one", value="cool")],
            False,
            False,
            id="should_not_raise_if_should_find_is_ok_with_str_value",
        ),
        pytest.param(
            {"cookie_one": "cool"},
            [Cookie(name="cookie_one", value=Regex("c.*"))],
            False,
            False,
            id="should_not_raise_if_should_find_is_ok_with_regex_value",
        ),
        pytest.param(
            {"cookie_one": "cool"},
            [Cookie(name="cookie_one", value=Text("cool"))],
            False,
            False,
            id="should_not_raise_if_should_find_is_ok_with_text_value",
        ),
        pytest.param(
            {"cookie_one": "cool"},
            [Cookie(name="cookie_one", value="ooops")],
            False,
            True,
            id="should_raise_if_should_find_is_ko_with_str_value",
        ),
        pytest.param(
            {"cookie_one": "cool"},
            [Cookie(name="cookie_one", value=Regex("ooops"))],
            False,
            True,
            id="should_raise_if_should_find_is_ko_with_regex_value",
        ),
        pytest.param(
            {"cookie_one": "cool"},
            [Cookie(name="cookie_one", value=Text("ooops"))],
            False,
            True,
            id="should_raise_if_should_find_is_ko_with_text_value",
        ),
        pytest.param(
            {"cookie_one": "cool"},
            [Cookie(name="cookie_one", value="ooops")],
            True,
            False,
            id="should_not_raise_if_should_not_find_is_ok_with_str_value",
        ),
        pytest.param(
            {"cookie_one": "cool"},
            [Cookie(name="cookie_one", value=Regex("^o.*"))],
            True,
            False,
            id="should_not_raise_if_should_not_find_is_ok_with_regex_value",
        ),
        pytest.param(
            {"cookie_one": "cool"},
            [Cookie(name="cookie_one", value=Text("ooops"))],
            True,
            False,
            id="should_not_raise_if_should_not_find_is_ok_with_text_value",
        ),
        pytest.param(
            {"cookie_one": "cool"},
            [Cookie(name="cookie_one", value="cool")],
            True,
            True,
            id="should_raise_if_should_not_find_is_ko_with_str_value",
        ),
        pytest.param(
            {"cookie_one": "cool"},
            [Cookie(name="cookie_one", value=Regex("o.*"))],
            True,
            True,
            id="should_raise_if_should_not_find_is_ko_with_regex_value",
        ),
        pytest.param(
            {"cookie_one": "cool"},
            [Cookie(name="cookie_one", value=Text("cool"))],
            True,
            True,
            id="should_raise_if_should_not_find_is_ko_with_text_value",
        ),
    ],
)
def test_page_checker_assert_cookies(
    http_client: Client,
    response_cookies: Sequence[SetCookie],
    expected_cookies: Sequence[Cookie],
    is_negative: bool,
    should_raise: bool,
    respx_mock: MockRouter,
):
    respx_mock.get("/test_page.html").respond(cookies=response_cookies)
    check = PageChecker(base_url="http://localhost", http_client=http_client)
    kwargs: Dict[str, Any] = {}
    if not is_negative:
        kwargs["should_find"] = Assertions(cookies=expected_cookies)
    else:
        kwargs["should_not_find"] = NegativeAssertions(cookies=expected_cookies)

    cm: AbstractContextManager
    if should_raise:
        cm = pytest.raises(AssertionError)
    else:
        cm = nullcontext()
    with cm:
        check(path="/test_page.html", title="from_unit_test", **kwargs)


@pytest.mark.parametrize(
    ["response_content", "expected_content", "is_negative", "should_raise"],
    [
        pytest.param(
            "hello world",
            "world",
            False,
            False,
            id="should_not_raise_if_should_find_is_ok_with_str_value",
        ),
        pytest.param(
            "hello world",
            Regex("w.*"),
            False,
            False,
            id="should_not_raise_if_should_find_is_ok_with_regex_value",
        ),
        pytest.param(
            "hello world",
            Text("world"),
            False,
            False,
            id="should_not_raise_if_should_find_is_ok_with_text_value",
        ),
        pytest.param(
            "hello world",
            ["world", Regex("w.*"), Text("world")],
            False,
            False,
            id="should_not_raise_if_should_find_is_ok_with_list_value",
        ),
        pytest.param(
            "hello world",
            "ooops",
            False,
            True,
            id="should_raise_if_should_find_is_ko_with_str_value",
        ),
        pytest.param(
            "hello world",
            Regex("oo.*"),
            False,
            True,
            id="should_raise_if_should_find_is_ko_with_regex_value",
        ),
        pytest.param(
            "hello world",
            Text("ooops"),
            False,
            True,
            id="should_raise_if_should_find_is_ko_with_text_value",
        ),
        pytest.param(
            "hello world",
            ["world", Regex("w.*"), Text("oops")],
            False,
            True,
            id="should_raise_if_should_find_is_ko_with_list_value",
        ),
        pytest.param(
            "hello world",
            "ooops",
            True,
            False,
            id="should_not_raise_if_should_not_find_is_ok_with_str_value",
        ),
        pytest.param(
            "hello world",
            Regex("oo.*"),
            True,
            False,
            id="should_not_raise_if_should_not_find_is_ok_with_regex_value",
        ),
        pytest.param(
            "hello world",
            Text("ooops"),
            True,
            False,
            id="should_not_raise_if_should_not_find_is_ok_with_text_value",
        ),
        pytest.param(
            "hello world",
            ["oops", Regex("oo.*"), Text("oops")],
            True,
            False,
            id="should_not_raise_if_should_not_find_is_ok_with_list_value",
        ),
        pytest.param(
            "hello world",
            "world",
            True,
            True,
            id="should_raise_if_should_not_find_is_ko_with_str_value",
        ),
        pytest.param(
            "hello world",
            Regex("w.*"),
            True,
            True,
            id="should_raise_if_should_not_find_is_ko_with_regex_value",
        ),
        pytest.param(
            "hello world",
            Text("world"),
            True,
            True,
            id="should_raise_if_should_not_find_is_ko_with_text_value",
        ),
        pytest.param(
            "hello world",
            ["ooops", Regex("oo.*"), Text("world")],
            True,
            True,
            id="should_raise_if_should_not_find_is_ko_with_list_value",
        ),
    ],
)
def test_page_checker_assert_content(
    http_client: Client,
    response_content: str,
    expected_content: Any,
    is_negative: bool,
    should_raise: bool,
    respx_mock: MockRouter,
):
    respx_mock.get("/test_page.html").respond(content=response_content)
    check = PageChecker(base_url="http://localhost", http_client=http_client)
    kwargs: Dict[str, Any] = {}
    if not is_negative:
        kwargs["should_find"] = Assertions(content=expected_content)
    else:
        kwargs["should_not_find"] = NegativeAssertions(content=expected_content)

    cm: AbstractContextManager
    if should_raise:
        cm = pytest.raises(AssertionError)
    else:
        cm = nullcontext()
    with cm:
        check(path="/test_page.html", title="from_unit_test", **kwargs)
