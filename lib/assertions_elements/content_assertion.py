import re
from typing import Optional, Sequence

from httpx import Client, Response

from .assert_element_base import AssertElementBase
from .assertion_base import AssertionBase


class _ContentAssertElement(AssertElementBase):
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


class ContentAssertion(AssertionBase):
    _assert_type = _ContentAssertElement
