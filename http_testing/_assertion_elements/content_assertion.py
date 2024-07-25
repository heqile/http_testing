import re
from typing import Sequence, Union

from http_testing.validators import Regex, Text, Validator

from .assert_element_checker_base import AssertElementCheckerBase
from .assertion_data import AssertionData


class ContentChecker(AssertElementCheckerBase[Union[str, Validator, Sequence[Union[str, Validator]]]]):
    """
    Check the response's content.
    If the given expected value is `str`, first convert it to `validators.Text` validator.
    If the given expected value is a `Regex` validator and its flag is 0, override the flag to `re.MULTILINE`
    """

    def __contains__(self, assertion_data: AssertionData) -> bool:
        if self.value is None:
            return True
        rules = [self.value] if isinstance(self.value, (str, Validator)) else self.value
        for expected in rules:
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

            if (not validator.validate(text=assertion_data.response_text)) ^ self.negative_assertion:
                self.assert_fail_description = self._make_message(
                    info=f"'{validator}'",
                    check_type="content",
                    url=str(assertion_data.url),
                )
                return False
        return True
