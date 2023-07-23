from httpx import Client, Response

from http_testing._assertion_elements.assertion_data import AssertionData

from .assert_element_checker_base import AssertElementCheckerBase
from .assertion_attribute_base import AssertionAttributeBase


class _StatusCodeChecker(AssertElementCheckerBase[int]):
    def check(self, http_client: Client, response: Response, negative: bool = False) -> None:
        assertion_request = AssertionData.create(response=response, http_client=http_client)
        if self.value:
            if (self.value != assertion_request.response_status_code) ^ negative:
                raise AssertionError(
                    self._make_message(
                        info=f"'{self.value}'",
                        check_type="status_code",
                        url=str(assertion_request.url),
                        negative=negative,
                    )
                )


class StatusCodeAssertion(AssertionAttributeBase):
    _checker_type = _StatusCodeChecker
