from http_testing._assertion_elements.assertion_data import AssertionData

from .assert_element_checker_base import AssertElementCheckerBase


class StatusCodeChecker(AssertElementCheckerBase[int]):
    def __contains__(self, assertion_data: AssertionData) -> bool:
        if not self.value:
            return True
        if (self.value != assertion_data.response_status_code) ^ self.negative_assertion:
            self.assert_fail_description = self._make_message(
                info=f"'{self.value}'",
                check_type="status_code",
                url=str(assertion_data.url),
            )
            return False
        return True
