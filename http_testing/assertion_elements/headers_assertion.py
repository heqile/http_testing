import re
from typing import Mapping

from httpx import Client, Response

from .assert_element_checker_base import AssertElementCheckerBase
from .assertion_attribute_base import AssertionAttributeBase


class _HeadersChecker(AssertElementCheckerBase[Mapping[str, str]]):
    def check(self, http_client: Client, response: Response, negative: bool = False) -> None:
        if self.value is None:
            return
        for header_key, header_value in self.value.items():
            # the header names in response are case-insensitive
            is_header_not_found = (
                header_key not in response.headers or re.search(header_value, response.headers[header_key]) is None
            )
            if is_header_not_found ^ negative:
                raise AssertionError(
                    self._make_message(
                        info=f"'{header_key}':'{header_value}'",
                        check_type="headers",
                        url=str(response.url),
                        negative=negative,
                    )
                )


class HeadersAssertion(AssertionAttributeBase):
    _checker_type = _HeadersChecker
