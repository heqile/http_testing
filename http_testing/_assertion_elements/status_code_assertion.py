from http_testing._assertion_elements.assertion_data import AssertionData

from .assert_element_checker_base import AssertElementCheckerBase
from .assertion_attribute_base import AssertionAttributeBase


class _StatusCodeChecker(AssertElementCheckerBase[int]):
    def check(self, assertion_data: AssertionData, negative: bool) -> None:
        if self.value:
            if (self.value != assertion_data.response_status_code) ^ negative:
                raise AssertionError(
                    self._make_message(
                        info=f"'{self.value}'",
                        check_type="status_code",
                        url=str(assertion_data.url),
                        negative=negative,
                    )
                )


class StatusCodeAssertion(AssertionAttributeBase):
    _checker_type = _StatusCodeChecker
