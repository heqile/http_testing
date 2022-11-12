from typing import Mapping, Optional, Sequence

from httpx import Client, Response

from .assertion_elements.assertion_attribute_base import check_all
from .assertion_elements.content_assertion import ContentAssertion
from .assertion_elements.cookies_assertion import Cookie, CookiesAssertion
from .assertion_elements.headers_assertion import HeadersAssertion
from .assertion_elements.status_code_assertion import StatusCodeAssertion


class _AssertionsBase:
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
        check_all(instance=self, http_client=http_client, response=response, negative=self._negative)


class Assertions(_AssertionsBase):
    _negative: bool = False


class NegativeAssertions(_AssertionsBase):
    _negative: bool = True
