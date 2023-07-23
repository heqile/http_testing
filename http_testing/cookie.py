from typing import Optional, Union

from attrs import define

from http_testing.validators import Validator


@define
class Cookie:
    name: str
    value: Union[str, Validator]
    domain: Optional[str] = None
    path: Optional[str] = None
    secure: Optional[bool] = None
    expires: Optional[int] = None
