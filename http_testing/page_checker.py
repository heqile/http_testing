from typing import Any, Dict, Optional, Union

from attrs import define
from httpx import URL, Client, Response

from http_testing._assertion_elements.assertion_data import AssertionData
from http_testing.assertions import Assertions, NegativeAssertions


@define
class PageChecker:
    _base_url: Union[URL, str]
    _http_client: Client
    _previous_response: Optional[Response] = None

    @property
    def previous_response(self) -> Response:
        if self._previous_response is None:
            raise RuntimeError("previous_response should be called following a http request")
        return self._previous_response

    def __call__(
        self,
        *,
        path: str,
        title: Optional[str] = None,
        base_url: Union[URL, str, None] = None,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        follow_redirects: bool = False,
        should_find: Optional[Assertions] = None,
        should_not_find: Optional[NegativeAssertions] = None,
        **kwargs: Any,
    ) -> None:
        """
        Call the target url with given arguments, then verify the response against given rules
        Return None if success, otherwise raise AssertionError
        """
        if base_url is None:
            base_url = self._base_url
        if isinstance(base_url, str):
            base_url = URL(base_url)

        response = self._http_client.request(
            method=method,
            url=base_url.copy_with(raw_path=path.encode("ascii")),
            data=data,
            headers=headers,
            cookies=cookies,
            follow_redirects=follow_redirects,
            **kwargs,
        )
        self._previous_response = response

        assertion_data = AssertionData.create(response=response, http_client=self._http_client, title=title)
        if should_find:
            should_find.check(assertion_data=assertion_data)
        if should_not_find:
            should_not_find.check(assertion_data=assertion_data)
