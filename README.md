# HTTP_TESTING

<a href="https://github.com/heqile/http_testing/actions?query=branch%3Amain+event%3Apush+" target="_blank">
    <img src="https://github.com/heqile/http_testing/workflows/Test/badge.svg?query=branch%3Amain+event%3Apush" alt="Test">
</a>
<a href="https://pypi.org/project/pytest-httptesting" target="_blank">
    <img src="https://img.shields.io/pypi/v/pytest-httptesting?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/pytest-httptesting" target="_blank">
    <img src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fheqile%2Fhttp_testing%2Fmain%2Fpyproject.toml" alt="Supported Python versions">
</a>

## Description
This project aims to help to create e2e tests, by chaining http calls and verifications on target pages.

## Concept
This project is built on pytest.

Each .py file in test represents several tests scenario on one target site, we can provide the site's hostname
as a local variable, the framework know how to construct http call from that.

Each test function in the .py test file represent a scenario of test which is consisted by several steps. For example,
test user's account page, first, we authenticate the client by post user's name and password,
then access the account page to verify some values. Each step is described by calling the variable `check`
which is a pytest fixture.

## Tutorial
### Install
```bash
pip install pytest-httptesting
```

### Create test suite
```python
# test/test_example.py
from http_testing.assertions import Assertions, NegativeAssertions
from http_testing.cookie import Cookie
from http_testing.page_checker import PageChecker
from http_testing.validators import Regex

host = "www.google.com"  # mandatory: used in the `check` fixture
scheme = "https"  # "https" by default
port = None  # None by default


def test_scenario_one(check: PageChecker):
    check(
        title="Scenario One",
        path="/",
        should_find=Assertions(
            status_code=200,
            content=["<title>Google</title>"],
            headers={"Content-Type": "text/html; charset=ISO-8859-1"},
            cookies=[Cookie(name="AEC", value=Regex(r".*"))],
        ),
        should_not_find=NegativeAssertions(
            status_code=400,
            content=["groot"],
            headers={"nooooo": ""},
            cookies=[Cookie(name="nop", value="a")],
        ),
        timeout=10,  # you can pass additional kwargs to httpx request
    )

    assert check.previous_response.status_code == 200  # inspect previous response
```

### Run test
```bash
$ pytest test --tb=short --no-header -v
============= test session starts =============
collected 1 item

test/test_example.py::test_scenario_one PASSED

============= 1 passed in 0.16s =============

```

### Debug
In case of error, a temporary file will be generated. It is a json file concluding
response content, status code, headers and cookies.
```bash
$ pytest test --tb=short --no-header -v
============= test session starts =============
collected 1 item

test/test_example.py::test_scenario_one FAILED
============= FAILURES =============
________ test_scenario_one _________
test/test_example.py:10: in test_scenario_one
    check(
http_testing/page_checker.py:62: in __call__
    should_find.check(assertion_data=assertion_data)
http_testing/assertions.py:33: in check
    assert assertion_data in checker
E   AssertionError: assert in check 'Senario One' - '<title>groot</title>' should found in content on page 'https://www.google.com/'
E         - please check file '/tmp/tmp3lp0d7oh'
============= short test summary info =============
FAILED test/test_example.py::test_scenario_one - AssertionError: assert in check 'Senario One' - '<title>groot</title>' should found in content on page 'https://www.google.com/'
============= 1 failed in 1.22s =============

```

### Advanced
#### Customize the http client configuration
It is possible to create a fixture `http_client` to create your own http client.
```python
@pytest.fixture
def http_client():
    with Client(verify=False, cookies={"cookie_1": "cookie_value_1"}) as client:
        yield client
```

#### Customize the base url
It is possible to create a fixture `base_url` to override the default construction of base url.
```python
from httpx import URL
@pytest.fixture
def base_url() -> URL:
    return URL("https://www.google.com")
```
