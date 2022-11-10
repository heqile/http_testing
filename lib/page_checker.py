from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from httpx import URL, Client

from .assertions import Assertions


class PageChecker:
    _base_url: URL
    _http_client: Client

    def __init__(self, base_url: URL):
        self._base_url = base_url
        self._http_client = Client(trust_env=False, verify=False)

    def __enter__(self) -> PageChecker:
        self._http_client.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._http_client.__exit__()

    def __call__(
        self,
        *,
        title: str,
        path: str,
        base_url: Optional[URL] = None,
        method: str = "GET",
        data: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        follow_redirects: bool = False,
        should_find: Optional[Dict] = None,
        should_not_find: Optional[Dict] = None,
        **_: Any,
    ) -> Any:
        base_url = base_url or self._base_url
        response = self._http_client.request(
            method=method,
            url=base_url.copy_with(raw_path=path.encode("ascii")),
            data=data,
            headers=headers,
            cookies=cookies,
            follow_redirects=follow_redirects,
        )
        try:
            if should_find:
                should_find_assertions = Assertions(**should_find)
                should_find_assertions.check_assertions(response=response)
            if should_not_find:
                should_not_find_assertions = Assertions(**should_not_find)
                should_not_find_assertions.check_assertions(response=response, negative=True)
        except AssertionError as exc:
            msg = f"{title} - {str(exc)}"
            logging.error(msg)
            raise AssertionError(msg) from exc
