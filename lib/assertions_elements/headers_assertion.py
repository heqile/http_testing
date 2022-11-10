import re
from typing import Mapping, Optional

from httpx import Client, Response

from .assert_element_base import AssertElementBase
from .assertion_base import AssertionBase


class _HeadersAssertElement(AssertElementBase):
    value: Optional[Mapping[str, str]]

    def check(self, _: Client, response: Response, negative: bool = False) -> None:
        if self.value is None:
            return
        for header_key, header_value in self.value.items():
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
        return


class HeadersAssertion(AssertionBase):
    _assert_type = _HeadersAssertElement