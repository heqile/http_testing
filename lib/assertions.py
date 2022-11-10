# type: ignore

from typing import Mapping, Optional, Sequence

from httpx import Client, Response

from .assertion_elements.content_assertion import ContentAssertion
from .assertion_elements.cookies_assertion import CookiesAssertion
from .assertion_elements.headers_assertion import HeadersAssertion
from .assertion_elements.status_code_assertion import StatusCodeAssertion
from .cookie import Cookie


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
        self.status_code.check(http_client, response, self._negative)
        self.content.check(http_client, response, self._negative)
        self.headers.check(http_client, response, self._negative)
        self.cookies.check(http_client, response, self._negative)


class Assertions(_AssertionsBase):
    _negative: bool = False


class NegativeAssertions(_AssertionsBase):
    _negative: bool = True
