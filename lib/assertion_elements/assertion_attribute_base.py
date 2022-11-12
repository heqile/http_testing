from typing import ClassVar, Type
from weakref import WeakKeyDictionary

from httpx import Client, Response

from .assert_element_checker_base import AssertElementCheckerBase


class AssertionAttributeBase:
    _checker_type: Type[AssertElementCheckerBase]
    # if the owner instance of the descriptor is deleted, we should also remove the its entry from assertion_instances
    # that's why we use WeakKeyDictionary
    assertion_instances: ClassVar[WeakKeyDictionary] = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if not hasattr(instance, self._private_name):
            return self._checker_type()
        return getattr(instance, self._private_name)

    def __set_name__(self, owner, name):
        self._private_name = f"_{name}"

    def __set__(self, instance, value):
        assertion_instance = self._checker_type(value)
        if instance not in self.assertion_instances:
            self.assertion_instances.setdefault(instance, [])
        self.assertion_instances[instance].append(assertion_instance)
        setattr(instance, self._private_name, assertion_instance)


def check_all(instance, http_client: Client, response: Response, negative: bool):
    assertion_instance: AssertElementCheckerBase
    for assertion_instance in AssertionAttributeBase.assertion_instances[instance]:
        assertion_instance.check(http_client, response, negative)
