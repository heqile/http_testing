from typing import Dict, Optional

from attrs import define


@define
class HttpClientConfiguration:
    headers: Optional[Dict[str, str]] = None
    cookies: Optional[Dict[str, str]] = None
    verify: bool = True
    trust_env: bool = True
