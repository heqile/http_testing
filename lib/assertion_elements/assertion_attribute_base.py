from typing import ClassVar, Type
from weakref import WeakKeyDictionary

from httpx import Client, Response

from .assert_element_checker_base import AssertElementCheckerBase


class AssertionAttributeBase:
    _checker_type: Type[AssertElementCheckerBase]
    # if the owner instance of the descriptor is deleted, we should also remove the its entry from assertion_instances
    # that's why we use WeakKeyDictionary
    # it groups the checkers by owner : {owner_instance: [checker_instance, ...]}
    checkers: ClassVar[WeakKeyDictionary] = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if not hasattr(instance, self._private_name):
            return self._checker_type()
        return getattr(instance, self._private_name)

    def __set_name__(self, owner, name):
        self._private_name = f"_{name}"

    def __set__(self, instance, value):
        checker = self._checker_type(value)
        if instance not in self.checkers:
            self.checkers.setdefault(instance, [])
        self.checkers[instance].append(checker)
        setattr(instance, self._private_name, checker)


def check_all(instance, http_client: Client, response: Response, negative: bool):
    checker: AssertElementCheckerBase
    for checker in AssertionAttributeBase.checkers[instance]:
        checker.check(http_client, response, negative)
