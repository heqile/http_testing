from httpx import Client, Response


class AssertElementCheckerBase:
    def __init__(self, value=None):
        self.value = value

    def check(self, http_client: Client, response: Response, negative: bool = False):
        raise NotImplementedError

    @staticmethod
    def _make_message(info: str, check_type: str, url: str, negative: bool) -> str:
        return f"{info}{'' if negative else ' not'} " f"found in {check_type} on page '{url}'"
