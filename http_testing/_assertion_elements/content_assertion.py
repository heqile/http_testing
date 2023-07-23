import re
from typing import Sequence, Union

from http_testing.validators import Regex, Text, Validator

from .assert_element_checker_base import AssertElementCheckerBase
from .assertion_attribute_base import AssertionAttributeBase
from .assertion_data import AssertionData


class _ContentChecker(AssertElementCheckerBase[Sequence[Union[str, Validator]]]):
    """
    Check the response's content.
    If the given expected value is `str`, first convert it to `validators.Text` validator.
    If the given expected value is a `Regex` validator and its flag is 0, override the flag to `re.MULTILINE`
    """

    def check(self, assertion_data: AssertionData, negative: bool) -> None:
        if self.value is None:
            return
        for expected in self.value:
            validator: Validator
            if isinstance(expected, str):
                validator = Text(value=expected)
            elif isinstance(expected, Regex):
                validator = expected
                if validator.flags == 0:
                    # prefer multiline mode when search in http content
                    validator.flags = re.MULTILINE
            else:
                validator = expected

            if (not validator.validate(text=assertion_data.response_text)) ^ negative:
                raise AssertionError(
                    self._make_message(
                        info=f"'{self.value}'", check_type="content", url=str(assertion_data.url), negative=negative
                    )
                )


class ContentAssertion(AssertionAttributeBase):
    _checker_type = _ContentChecker
