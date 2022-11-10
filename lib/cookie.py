from dataclasses import dataclass
from typing import Optional


@dataclass
class Cookie:
    name: str
    value_pattern: str
    domain: Optional[str] = None
    path: Optional[str] = None
    secure: Optional[bool] = None
    expires: Optional[str] = None
