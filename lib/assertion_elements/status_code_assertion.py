from httpx import Client, Response

from .assert_element_checker_base import AssertElementCheckerBase
from .assertion_attribute_base import AssertionAttributeBase


class _StatusCodeChecker(AssertElementCheckerBase[int]):
    def check(self, http_client: Client, response: Response, negative: bool = False) -> None:
        if self.value:
            if (self.value != response.status_code) ^ negative:
                raise AssertionError(
                    self._make_message(
                        info=f"'{self.value}'", check_type="status_code", url=str(response.url), negative=negative
                    )
                )


class StatusCodeAssertion(AssertionAttributeBase):
    _checker_type = _StatusCodeChecker
