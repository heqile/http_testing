from http_testing._assertion_elements.assert_element_checker_base import AssertElementCheckerBase
from http_testing._assertion_elements.assertion_attribute_base import AssertionAttributeBase
from http_testing._assertion_elements.assertion_data import AssertionData


class SampleAssertElement(AssertElementCheckerBase):
    def __contains__(self, assertion_data: AssertionData) -> bool:
        return True


class SampleAssertion(AssertionAttributeBase):
    _checker_type = SampleAssertElement


class Sample:
    a = SampleAssertion()


def test_remove_assertion_instances_entry_if_owner_obj_is_deleted():
    obj = Sample()
    obj.a = 1
    assert len(AssertionAttributeBase.checkers) == 1
    del obj
    assert len(AssertionAttributeBase.checkers) == 0
