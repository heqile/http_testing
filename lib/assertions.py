from dataclasses import dataclass
from typing import Mapping, Optional, Sequence

from httpx import Response


@dataclass
class Assertions:
    content: Optional[Sequence[str]] = None
    headers: Optional[Mapping[str, str]] = None
    cookies: Optional[Mapping[str, str]] = None

    def check_assertions(self, response: Response, negative: bool = False) -> bool:
        if self.content:
            for content in self.content:
                if (content not in response.text) ^ negative:
                    return False
        if self.headers:
            for header_key, header_value in self.headers.items():
                if (not response.headers.get(header_key) == header_value) ^ negative:
                    return False
        if self.cookies:
            for cookie_key, cookie_value in self.cookies.items():
                if (not response.cookies.get(cookie_key) == cookie_value) ^ negative:
                    return False
        return True
