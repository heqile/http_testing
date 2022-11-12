from typing import Optional

from httpx import Client, Response

from .assert_element_base import AssertElementBase
from .assertion_attribute_base import AssertionAttributeBase


class _StatusCodeAssertElement(AssertElementBase):
    value: Optional[int]

    def check(self, _: Client, response: Response, negative: bool = False) -> None:
        if self.value:
            if (self.value != response.status_code) ^ negative:
                raise AssertionError(
                    self._make_message(
                        info=f"'{self.value}'", check_type="status_code", url=str(response.url), negative=negative
                    )
                )


class StatusCodeAssertion(AssertionAttributeBase):
    _assert_type = _StatusCodeAssertElement
