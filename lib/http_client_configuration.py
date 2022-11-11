from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class HttpClientConfiguration:
    headers: Optional[Dict[str, str]] = None
    cookies: Optional[Dict[str, str]] = None
    verify: bool = True
    trust_env: bool = True
