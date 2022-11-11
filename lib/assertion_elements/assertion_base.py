from collections import defaultdict
from typing import Any, Dict

from httpx import Client, Response


class AssertionBase:
    _assert_type: Any = None
    assertion_instances: Dict[int, Any] = defaultdict(list)

    def __get__(self, instance, owner):
        if not hasattr(instance, self._private_name):
            return self._assert_type()
        return getattr(instance, self._private_name)

    def __set_name__(self, owner, name):
        self._private_name = f"_{name}"

    def __set__(self, instance, value):
        assertion_instance = self._assert_type(value)
        self.assertion_instances[id(instance)].append(assertion_instance)
        setattr(instance, self._private_name, assertion_instance)


def check_all(instance, http_client: Client, response: Response, negative: bool):
    for assertion_instance in AssertionBase.assertion_instances[id(instance)]:
        getattr(assertion_instance, "check")(http_client, response, negative)
