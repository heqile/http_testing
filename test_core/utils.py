from dataclasses import dataclass
from typing import Any


@dataclass
class Spec:
    negative: Any
    expected: Any
