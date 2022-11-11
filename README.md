# HTTP_TESTING

## Description
This project aims to help to create e2e tests, by chaining http calls and verifications on target pages.
IMPORTANT: Since only http calls involved, no javascript will run.

## Concept
This project is built on pytest.

Each .py file in test represents several tests scenario on one target site, we can provide the site's hostname
as a local variable, the framework know how to construct http call from that.

Each test function in the .py test file represent a scenario of test which is consisted by several steps. For example,
test user's account page, first, we authenticate the client by post user's name and password,
then access the account page to verify some values. Each step is described by calling the variable `check`
which is a pytest fixture.

## Tutorial
### Create test suite
```python
# test/test_example.py

from lib.assertion_elements.cookies_assertion import CookieP
from lib.assertions import Assertions, NegativeAssertions
from lib.page_checker import PageChecker

host = "www.google.com"  # madatory: used in the `check` fixture
scheme = "https"  # "https" by default
port = None  # None by default


def test_scenario_one(check: PageChecker):
    check(
        title="Senario One",
        path="/",
        should_find=Assertions(
            status_code=200,
            content=["<title>Google</title>"],
            headers={"Content-Type": "text/html; charset=ISO-8859-1"},
            cookies=[Cookie(name="AEC", value_pattern=r".*")],
        ),
        should_not_find=NegativeAssertions(
            status_code=400,
            content=["groot"],
            headers={"nooooo": ""},
            cookies=[Cookie(name="nop", value_pattern="a")],
        ),
    )
```

### Run test
```bash
$ pytest --tb=no test  # traceback is disabled because it is not very useful to anayse the functional error
============= test session starts =============
platform linux -- Python 3.8.10, pytest-7.2.0, pluggy-1.0.0
rootdir: /home/xxx/workspace/http_testing
plugins: anyio-3.6.2
collected 1 items

test/test_example.py .                                                                  [100%]

=============  1 passed in 0.22s =============

```

### Debug
In case of error, a temporary file will be generated, as shown in the `test summary info`. It is a json file concluding
response content, status code, headers and cookies.
```bash
$ pytest --tb=no test
============= test session starts =============
platform linux -- Python 3.8.10, pytest-7.2.0, pluggy-1.0.0
rootdir: /home/qile/workspace/http_testing
plugins: anyio-3.6.2
collected 1 item

test/test_example.py F                                                                  [100%]

============= short test summary info =============
FAILED test/test_example.py::test_scenario_one - AssertionError: Senario One - 'Content-Typesssssss':'text/html; charset=ISO-8859-1' not found in headers on page 'https://www.google.com/' - please check file '/tmp/tmpx7zb7h16'
============= 1 failed in 0.25s =============

```

### Advanced
#### Customize the http client configuration
We can create a fixture `http_client_config` to override the default configuration, like adding headers and cookies to the http client.
```python
@pytest.fixture
def http_client_config():
    return HttpClientConfiguration(
        trust_env=False,
        verify=False,
        cookies={"cookie_1": "cookie_value_1"},
        headers={"header_1": "header_value_1"},
    )
```
