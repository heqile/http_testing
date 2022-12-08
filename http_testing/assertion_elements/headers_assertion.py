from typing import Mapping, Union

from httpx import Client, Response

from ..validators import Text, Validator
from .assert_element_checker_base import AssertElementCheckerBase
from .assertion_attribute_base import AssertionAttributeBase


class _HeadersChecker(AssertElementCheckerBase[Mapping[str, Union[str, Validator]]]):
    def check(self, http_client: Client, response: Response, negative: bool = False) -> None:
        """
        Check the response's header.
        If the given expected header value is `str`, first convert it to `validators.Text` validator.
        """
        if self.value is None:
            return
        for header_key, expected_header_value in self.value.items():
            validator: Validator
            if isinstance(expected_header_value, str):
                validator = Text(value=expected_header_value)
            else:
                validator = expected_header_value
            # the header names in response are case-insensitive
            is_header_not_found = header_key not in response.headers or not validator.validate(
                response.headers[header_key]
            )
            if is_header_not_found ^ negative:
                raise AssertionError(
                    self._make_message(
                        info=f"'{header_key}':'{expected_header_value}'",
                        check_type="headers",
                        url=str(response.url),
                        negative=negative,
                    )
                )


class HeadersAssertion(AssertionAttributeBase):
    _checker_type = _HeadersChecker
