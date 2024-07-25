from attrs import define
from httpx import Request, Response


@define
class RecordData:
    title: str
    request: Request
    response: Response
