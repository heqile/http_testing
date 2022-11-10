from typing import Any


class AssertionBase:
    _assert_type: Any = None

    def __get__(self, instance, owner):
        if not hasattr(instance, self._private_name):
            return self._assert_type()
        return getattr(instance, self._private_name)

    def __set_name__(self, owner, name):
        self._private_name = f"_{name}"

    def __set__(self, instance, value):
        setattr(instance, self._private_name, self._assert_type(value))
