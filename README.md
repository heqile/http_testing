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
Check the file `test/test_example.py`
