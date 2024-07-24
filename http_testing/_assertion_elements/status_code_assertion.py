from http_testing._assertion_elements.assertion_data import AssertionData

from .assert_element_checker_base import AssertElementCheckerBase
from .assertion_attribute_base import AssertionAttributeBase


class _StatusCodeChecker(AssertElementCheckerBase[int]):
    def __contains__(self, assertion_data: AssertionData) -> bool:
        if not self.value:
            return True
        if (self.value != assertion_data.response_status_code) ^ assertion_data.negative_assertion:
            self.assert_fail_description = self._make_message(
                info=f"'{self.value}'",
                check_type="status_code",
                url=str(assertion_data.url),
                negative=assertion_data.negative_assertion,
            )
            return False
        return True


class StatusCodeAssertion(AssertionAttributeBase):
    _checker_type = _StatusCodeChecker
