import re
from typing import Optional, Sequence

from httpx import Client, Response

from .assert_element_checker_base import AssertElementCheckerBase
from .assertion_attribute_base import AssertionAttributeBase


class _ContentChecker(AssertElementCheckerBase):
    value: Optional[Sequence[str]]

    def check(self, _: Client, response: Response, negative: bool = False) -> None:
        if self.value is None:
            return
        for content in self.value:
            if (re.search(content, response.text, re.MULTILINE) is None) ^ negative:
                raise AssertionError(
                    self._make_message(
                        info=f"'{self.value}'", check_type="content", url=str(response.url), negative=negative
                    )
                )
        return


class ContentAssertion(AssertionAttributeBase):
    _checker_type = _ContentChecker
