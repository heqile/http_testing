# HTTP_TESTING

## Description
This project aims to help create suite of tests, by chaining calls of pages and verification.

## Concept
This project is built on pytest.

Each .py file in test represents one target site, we can provide the site's hostname
as a local variable, the framework know how to construct http call from that.

Each test function in the .py test file represent a scenario of test which is consisted by several steps. For example,
test user's account page, first, we authenticate the client by post user's name and password,
then access the account page to verify some values. Of course, we can have several scenario in one test file.

### Create test suite
```python
# test_example.py

schema = "https"
host = "example.com"
port = 80

def test_scenario_one(run_test):
    run_test(title="login", base_url=None, url="/login", method="POST", data={"login": "test", "password": "123456"}, headers={}, cookies={}, follow=False, should_find=["ok", r"test"], should_not_find=["fail"])
    run_test(title="account", url="/account", should_find=["1"])

```

## API
### run_test
```python

```
