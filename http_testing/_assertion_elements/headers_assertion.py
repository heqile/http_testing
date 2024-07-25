from typing import Mapping, Union

from http_testing.validators import Text, Validator

from .assert_element_checker_base import AssertElementCheckerBase
from .assertion_data import AssertionData


class HeadersChecker(AssertElementCheckerBase[Mapping[str, Union[str, Validator]]]):
    def __contains__(self, assertion_data: AssertionData) -> bool:
        """
        Check the response's header.
        If the given expected header value is `str`, first convert it to `validators.Text` validator.
        """
        if self.value is None:
            return True
        for header_key, expected_header_value in self.value.items():
            header_key = header_key.upper()
            validator: Validator
            if isinstance(expected_header_value, str):
                validator = Text(value=expected_header_value)
            else:
                validator = expected_header_value
            is_header_not_found = header_key not in assertion_data.response_headers or not validator.validate(
                assertion_data.response_headers[header_key]
            )
            if is_header_not_found ^ self.negative_assertion:
                self.assert_fail_description = self._make_message(
                    info=f"'{header_key}':'{expected_header_value}'",
                    check_type="headers",
                    url=str(assertion_data.url),
                )
                return False
        return True
