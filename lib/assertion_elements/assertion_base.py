from collections import defaultdict
from typing import Dict, List, Type
from weakref import finalize

from httpx import Client, Response

from .assert_element_base import AssertElementBase


class AssertionBase:
    _assert_type: Type[AssertElementBase]
    assertion_instances: Dict[int, List[AssertElementBase]] = defaultdict(list)

    def __get__(self, instance, owner):
        if not hasattr(instance, self._private_name):
            return self._assert_type()
        return getattr(instance, self._private_name)

    def __set_name__(self, owner, name):
        self._private_name = f"_{name}"

    def __set__(self, instance, value):
        assertion_instance = self._assert_type(value)
        dict_key = get_dict_key(instance)
        self.assertion_instances[dict_key].append(assertion_instance)
        setattr(instance, self._private_name, assertion_instance)
        finalize(instance, self._remove_assertion_instance, dict_key)  # remove the entry when instance is deleted

    def _remove_assertion_instance(self, key):
        if key in self.assertion_instances:
            del self.assertion_instances[key]


def get_dict_key(instance):
    return id(instance)


def check_all(instance, http_client: Client, response: Response, negative: bool):
    for assertion_instance in AssertionBase.assertion_instances[get_dict_key(instance)]:
        assertion_instance.check(http_client, response, negative)
