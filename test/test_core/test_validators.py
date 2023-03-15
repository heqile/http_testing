from http_testing.validators import Regex, Text


def test_regex_validator_should_ok():
    regex_validator = Regex(pattern=r"test \' ok \$ ")
    assert regex_validator.validate(text="first test ' ok $ end")


def test_regex_validator_should_fail_when_not_match():
    regex_validator = Regex(pattern="test ' ok $ ")
    assert regex_validator.validate(text="first end") is False


def test_text_validator_should_ok():
    text_validator = Text(value="test")
    assert text_validator.validate(text="now test me")


def test_text_validator_should_fail_when_not_match():
    text_validator = Text(value="test")
    assert text_validator.validate(text="now") is False
