from typing import Any

from attrs import define


@define
class Spec:
    negative: Any
    expected: Any
