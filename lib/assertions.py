import re
from dataclasses import dataclass
from typing import Mapping, Optional, Sequence

from httpx import Response


@dataclass
class Assertions:
    content: Optional[Sequence[str]] = None
    headers: Optional[Mapping[str, str]] = None
    cookies: Optional[Mapping[str, str]] = None

    def check_assertions(self, response: Response, negative: bool = False) -> None:
        if self.content:
            for content in self.content:
                if (re.search(content, response.text, re.MULTILINE) is None) ^ negative:
                    msg = f"'{content}'{'' if negative else ' not'} found on page '{response.url}'"
                    raise AssertionError(msg)
        if self.headers:
            for header_key, header_value in self.headers.items():
                if (
                    header_key not in response.headers or re.search(header_value, response.headers[header_key]) is None
                ) ^ negative:
                    msg = (
                        f"'{header_key}':'{header_value}'{'' if negative else ' not'} "
                        "found in headers on page '{response.url}'"
                    )
                    raise AssertionError(msg)
        if self.cookies:
            for cookie_key, cookie_value in self.cookies.items():
                if (
                    cookie_key not in response.cookies or re.search(cookie_value, response.cookies[cookie_key]) is None
                ) ^ negative:
                    msg = (
                        f"'{cookie_key}':'{cookie_value}'{'' if negative else ' not'} "
                        "found in headers on page '{response.url}'"
                    )
                    raise AssertionError(msg)
