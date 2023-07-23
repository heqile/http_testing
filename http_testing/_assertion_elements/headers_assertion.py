from typing import Mapping, Union

from httpx import Client, Response

from http_testing._assertion_elements.assertion_data import AssertionData

from ..validators import Text, Validator
from .assert_element_checker_base import AssertElementCheckerBase
from .assertion_attribute_base import AssertionAttributeBase


class _HeadersChecker(AssertElementCheckerBase[Mapping[str, Union[str, Validator]]]):
    def check(self, http_client: Client, response: Response, negative: bool = False) -> None:
        """
        Check the response's header.
        If the given expected header value is `str`, first convert it to `validators.Text` validator.
        """
        assertion_request = AssertionData.create(response=response, http_client=http_client)
        if self.value is None:
            return
        for header_key, expected_header_value in self.value.items():
            header_key = header_key.upper()
            validator: Validator
            if isinstance(expected_header_value, str):
                validator = Text(value=expected_header_value)
            else:
                validator = expected_header_value
            is_header_not_found = header_key not in assertion_request.response_headers or not validator.validate(
                assertion_request.response_headers[header_key]
            )
            if is_header_not_found ^ negative:
                raise AssertionError(
                    self._make_message(
                        info=f"'{header_key}':'{expected_header_value}'",
                        check_type="headers",
                        url=str(assertion_request.url),
                        negative=negative,
                    )
                )


class HeadersAssertion(AssertionAttributeBase):
    _checker_type = _HeadersChecker
