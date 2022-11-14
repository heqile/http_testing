import json
from tempfile import NamedTemporaryFile
from typing import Any, Dict, Optional

from httpx import URL, Client, Response

from .assertions import Assertions, NegativeAssertions


class PageChecker:
    _base_url: URL
    _http_client: Client

    def __init__(self, http_client: Client, base_url: URL):
        self._base_url = base_url
        self._http_client = http_client

    def __call__(
        self,
        *,
        path: str,
        title: Optional[str] = None,
        base_url: Optional[URL] = None,
        method: str = "GET",
        data: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        follow_redirects: bool = False,
        should_find: Optional[Assertions] = None,
        should_not_find: Optional[NegativeAssertions] = None,
        **_: Any,
    ) -> None:
        """
        Call the target url with given arguments, then verify the response against given rules
        Return None if success, otherwise raise AssertionError
        """
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
                should_find.check_assertions(http_client=self._http_client, response=response)
            if should_not_find:
                should_not_find.check_assertions(http_client=self._http_client, response=response)
        except AssertionError as exc:
            file_name = self._dump_response(response=response)
            prefix = f"{title} - " if title else ""
            msg = f"{prefix}{str(exc)} - please check file '{file_name}'"
            raise AssertionError(msg) from exc

    @staticmethod
    def _dump_response(response: Response) -> str:
        """
        Save the response's essential contents into a temporay file
        Return the file name
        """
        result: Dict[str, Any] = {
            "status_code": response.status_code,
            "content": response.text,
            "headers": dict(response.headers),
            "cookies": dict(response.cookies),
        }
        with NamedTemporaryFile(mode="wt", delete=False) as f:
            json.dump(obj=result, fp=f, indent=4)
            return f.name
