from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from http_testing._assertion_elements.assertion_data import AssertionData

T = TypeVar("T")


class AssertElementCheckerBase(Generic[T], ABC):
    value: Optional[T]
    assert_fail_description: Optional[str] = None

    def __init__(self, value: Optional[T] = None):
        self.value = value

    @abstractmethod
    def __contains__(self, assertion_data: AssertionData) -> bool:
        """
        in order to make better assertion report by pytest_assertrepr_compare, use `in` operator
        """
        raise NotImplementedError

    @staticmethod
    def _make_message(info: str, check_type: str, url: str, negative: bool) -> str:
        return f"{info} {'should not' if negative else 'should'} " f"found in {check_type} on page '{url}'"
