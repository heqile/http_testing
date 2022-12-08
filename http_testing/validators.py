import re
from typing import Protocol, Union

from attrs import define


class Validator(Protocol):
    def validate(self, text: str) -> bool:
        ...


@define
class Regex(Validator):
    """
    Used to validate some text with given regex pattern. The defaul flag=0 means no flag.
    """

    pattern: str
    flags: Union[int, re.RegexFlag] = 0

    def validate(self, text: str) -> bool:
        return re.search(self.pattern, text, flags=self.flags) is not None


@define
class Text(Validator):
    """
    Used to validate some text by check if it contains given value
    """

    value: str

    def validate(self, text: str) -> bool:
        return self.value in text
