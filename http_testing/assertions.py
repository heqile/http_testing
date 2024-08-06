from abc import ABC
from typing import ClassVar, Mapping, Optional, Sequence, Union

from http_testing._assertion_elements.assert_element_checker_base import AssertElementCheckerBase
from http_testing._assertion_elements.assertion_data import AssertionData
from http_testing._assertion_elements.content_assertion import ContentChecker
from http_testing._assertion_elements.cookies_assertion import Cookie, CookiesChecker
from http_testing._assertion_elements.headers_assertion import HeadersChecker
from http_testing._assertion_elements.status_code_assertion import StatusCodeChecker
from http_testing.validators import Validator


class _AssertionsBase(ABC):
    _negative_assertion: ClassVar[bool]
    _assert_checkers: Sequence[AssertElementCheckerBase]

    def __init__(
        self,
        status_code: Optional[int] = None,
        content: Union[None, str, Validator, Sequence[Union[str, Validator]]] = None,
        headers: Optional[Mapping[str, Union[str, Validator]]] = None,
        cookies: Optional[Sequence[Cookie]] = None,
    ):
        self._assert_checkers = [
            StatusCodeChecker(value=status_code, negative_assertion=self._negative_assertion),
            ContentChecker(value=content, negative_assertion=self._negative_assertion),
            HeadersChecker(value=headers, negative_assertion=self._negative_assertion),
            CookiesChecker(value=cookies, negative_assertion=self._negative_assertion),
        ]

    def check(self, assertion_data: AssertionData) -> None:
        for checker in self._assert_checkers:
            assert assertion_data in checker


class Assertions(_AssertionsBase):
    _negative_assertion: ClassVar[bool] = False


class NegativeAssertions(_AssertionsBase):
    _negative_assertion: ClassVar[bool] = True
