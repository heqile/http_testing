from lib.assertion_elements.assert_element_base import AssertElementBase
from lib.assertion_elements.assertion_attribute_base import AssertionAttributeBase


class SampleAssertElement(AssertElementBase):
    ...


class SampleAssertion(AssertionAttributeBase):
    _assert_type = SampleAssertElement


class Sample:
    a = SampleAssertion()


def test_remove_assertion_instances_entry_if_owner_obj_is_deleted():
    obj = Sample()
    obj.a = 1
    assert len(AssertionAttributeBase.assertion_instances) == 1
    del obj
    assert len(AssertionAttributeBase.assertion_instances) == 0
