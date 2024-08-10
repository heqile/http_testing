import secrets
from typing import Any, Dict, List, Mapping, Optional, Union

from attrs import define, field
from httpx import URL, Client, Response

from http_testing._assertion_elements.assertion_data import AssertionData
from http_testing._record import RecordData
from http_testing.assertions import Assertions, NegativeAssertions


@define
class PageChecker:
    _base_url: Union[URL, str]
    _http_client: Client
    history: List[RecordData] = field(factory=list, init=False)

    @property
    def previous_response(self) -> Response:
        if not self.history:
            raise RuntimeError("previous_response should be called following a http request")
        return self.history[-1].response

    def __call__(
        self,
        *,
        path: str,
        title: Optional[str] = None,
        base_url: Union[URL, str, None] = None,
        method: str = "GET",
        params: Optional[Mapping[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        content: Union[str, bytes, None] = None,
        json: Optional[Any] = None,
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
        url = base_url.copy_with(raw_path=path.encode("ascii"))
        title = title or f"{url}-{secrets.token_hex(5)}"
        request = self._http_client.build_request(
            method=method,
            url=url,
            data=data,
            headers=headers,
            cookies=cookies,
            params=params,
            content=content,
            json=json,
            **kwargs,
        )
        response = self._http_client.send(request=request, follow_redirects=follow_redirects)
        self.history.append(RecordData(title=title, request=request, response=response))

        assertion_data = AssertionData.create(response=response, title=title)
        if should_find:
            should_find.check(assertion_data=assertion_data)
        if should_not_find:
            should_not_find.check(assertion_data=assertion_data)
