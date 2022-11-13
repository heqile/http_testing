from http_testing.assertion_elements.cookies_assertion import Cookie
from http_testing.assertions import Assertions, NegativeAssertions
from http_testing.page_checker import PageChecker

host = "www.google.com"


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
