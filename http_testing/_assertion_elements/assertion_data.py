from __future__ import annotations

from collections import defaultdict
from http.cookiejar import Cookie as HttpCookie
from typing import Mapping, Optional, Sequence, Union

from attrs import frozen
from httpx import URL, Response


@frozen(kw_only=True)
class HttpClientCookie:
    name: str
    value: Optional[str]
    domain: Optional[str] = None
    path: Optional[str] = None
    secure: bool
    expires: Optional[int] = None

    @staticmethod
    def create(cookie: HttpCookie) -> HttpClientCookie:
        return HttpClientCookie(
            name=cookie.name,
            value=cookie.value,
            domain=cookie.domain if cookie.domain_specified else None,
            path=cookie.path if cookie.path_specified else None,
            secure=cookie.secure,
            expires=cookie.expires,
        )


@frozen(kw_only=True)
class AssertionData:
    url: Union[str, URL]
    all_cookies: Mapping[str, Sequence[HttpClientCookie]]
    response_status_code: int
    response_headers: Mapping[str, str]
    response_text: str
    title: Optional[str] = None  # used to generate assert report
    response: Optional[Response] = None  # used to generate log file

    @staticmethod
    def create(title: str, response: Response) -> AssertionData:
        all_cookies = defaultdict(list)
        for cookie in response.cookies.jar:
            all_cookies[cookie.name].append(HttpClientCookie.create(cookie))
        return AssertionData(
            url=response.url,
            all_cookies=all_cookies,
            response_headers={key.upper(): value for key, value in response.headers.items()},
            response_status_code=response.status_code,
            response_text=response.text,
            response=response,
            title=title,
        )
