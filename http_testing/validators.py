import re
from abc import ABC, abstractmethod
from typing import Union

from attrs import define


class Validator(ABC):
    @abstractmethod
    def validate(self, text: str) -> bool:
        raise NotImplementedError


@define
class Regex(Validator):
    """
    Used to validate some text with given regex pattern. The defaul flag=0 means no flag.
    """

    pattern: str
    flags: Union[int, re.RegexFlag] = 0

    def __str__(self) -> str:
        return f"pattern({self.pattern}) with flags({self.flags})"

    def validate(self, text: str) -> bool:
        return re.search(self.pattern, text, flags=self.flags) is not None


@define
class Text(Validator):
    """
    Used to validate some text by check if it contains given value
    """

    value: str

    def __str__(self):
        return f"{self.value}"

    def validate(self, text: str) -> bool:
        return self.value in text
