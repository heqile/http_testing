from abc import ABC
from typing import Mapping, Optional, Sequence

from httpx import Client, Response

from http_testing._assertion_elements.assertion_attribute_base import check_all
from http_testing._assertion_elements.assertion_data import AssertionData
from http_testing._assertion_elements.content_assertion import ContentAssertion
from http_testing._assertion_elements.cookies_assertion import Cookie, CookiesAssertion
from http_testing._assertion_elements.headers_assertion import HeadersAssertion
from http_testing._assertion_elements.status_code_assertion import StatusCodeAssertion


class _AssertionsBase(ABC):
    _negative: bool = False
    status_code = StatusCodeAssertion()
    content = ContentAssertion()
    headers = HeadersAssertion()
    cookies = CookiesAssertion()

    def __init__(
        self,
        status_code: Optional[int] = None,
        content: Optional[Sequence[str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        cookies: Optional[Sequence[Cookie]] = None,
    ):
        self.status_code = status_code
        self.content = content
        self.headers = headers
        self.cookies = cookies

    def check_assertions(self, http_client: Client, response: Response) -> None:
        assertion_data = AssertionData.create(response=response, http_client=http_client)
        check_all(instance=self, assertion_data=assertion_data, negative=self._negative)


class Assertions(_AssertionsBase):
    _negative: bool = False


class NegativeAssertions(_AssertionsBase):
    _negative: bool = True
