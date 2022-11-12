from lib.assertion_elements.assert_element_base import AssertElementBase
from lib.assertion_elements.assertion_base import AssertionBase


class SampleAssertElement(AssertElementBase):
    ...


class SampleAssertion(AssertionBase):
    _assert_type = SampleAssertElement


class Sample:
    a = SampleAssertion()


def test_remove_assertion_instances_entry_if_owner_obj_is_deleted():
    obj = Sample()
    obj.a = 1
    assert len(AssertionBase.assertion_instances) == 1
    del obj
    assert len(AssertionBase.assertion_instances) == 0
