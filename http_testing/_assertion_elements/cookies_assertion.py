from typing import Mapping, Sequence

from http_testing.cookie import Cookie
from http_testing.validators import Text, Validator

from .assert_element_checker_base import AssertElementCheckerBase
from .assertion_attribute_base import AssertionAttributeBase
from .assertion_data import AssertionData, HttpClientCookie


class _CookiesChecker(AssertElementCheckerBase[Sequence[Cookie]]):
    def check(self, assertion_data: AssertionData, negative: bool) -> None:
        if self.value is None:
            return
        for cookie in self.value:
            is_cookie_exist = self._is_cookie_match(target_cookie=cookie, all_cookies=assertion_data.all_cookies)
            if (not is_cookie_exist) ^ negative:
                raise AssertionError(
                    self._make_message(
                        info=f"'{cookie.name}':'{cookie.value}'",
                        check_type="cookies",
                        url=str(assertion_data.url),
                        negative=negative,
                    )
                )

    @staticmethod
    def _is_cookie_match(target_cookie: Cookie, all_cookies: Mapping[str, Sequence[HttpClientCookie]]):
        cookies = all_cookies.get(target_cookie.name)
        if cookies is None:
            return False
        for cookie in cookies:
            if cookie.value is None:
                continue
            if target_cookie.domain is not None and cookie.domain is not None and target_cookie.domain != cookie.domain:
                continue
            if target_cookie.path is not None and cookie.path is not None and target_cookie.path != cookie.path:
                continue
            if target_cookie.secure is not None and target_cookie.secure != cookie.secure:
                continue
            if (
                target_cookie.expires is not None
                and cookie.expires is not None
                and target_cookie.expires != cookie.expires
            ):
                continue
            validator: Validator
            if isinstance(target_cookie.value, str):
                validator = Text(value=target_cookie.value)
            else:
                validator = target_cookie.value
            if validator.validate(cookie.value):
                return True
        return False


class CookiesAssertion(AssertionAttributeBase):
    _checker_type = _CookiesChecker
