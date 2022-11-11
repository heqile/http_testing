import re
from collections import defaultdict
from http.cookiejar import Cookie as HttpCookie
from typing import Mapping, Optional, Sequence

from httpx import Client, Response

from ..cookie import Cookie
from .assert_element_base import AssertElementBase
from .assertion_base import AssertionBase


class _CookiesAssertElement(AssertElementBase):
    value: Optional[Sequence[Cookie]]

    def check(self, http_client: Client, response: Response, negative: bool = False) -> None:
        if self.value is None:
            return
        for cookie in self.value:
            all_cookies = defaultdict(list)  # same cookie name can be on different sites
            for cookiejar in http_client.cookies.jar:
                all_cookies[cookiejar.name].append(cookiejar)
            for cookiejar in response.cookies.jar:
                all_cookies[cookiejar.name].append(cookiejar)

            is_cookie_exist = self._is_cookie_match(target_cookie=cookie, all_cookies=all_cookies)
            if (not is_cookie_exist) ^ negative:
                raise AssertionError(
                    self._make_message(
                        info=f"'{cookie.name}':'{cookie.value_pattern}'",
                        check_type="cookies",
                        url=str(response.url),
                        negative=negative,
                    )
                )

    @staticmethod
    def _is_cookie_match(target_cookie: Cookie, all_cookies: Mapping[str, Sequence[HttpCookie]]):
        cookies = all_cookies.get(target_cookie.name)
        if cookies is None:
            return False
        for cookie in cookies:
            if cookie.value is None:
                continue
            if target_cookie.domain is not None and cookie.domain_specified and target_cookie.domain != cookie.domain:
                continue
            if target_cookie.path is not None and cookie.path_specified and target_cookie.path != cookie.path:
                continue
            if target_cookie.secure is not None and target_cookie.secure != cookie.secure:
                continue
            if target_cookie.expires is not None and target_cookie.expires != cookie.expires:
                continue
            if re.search(target_cookie.value_pattern, cookie.value) is not None:
                return True
        return False


class CookiesAssertion(AssertionBase):
    _assert_type = _CookiesAssertElement