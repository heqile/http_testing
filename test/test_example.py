from lib.page_checker import PageChecker

host = "www.google.com"


def test_scenario_one(check: PageChecker):
    check(
        title="Senario One",
        path="/",
        should_find={
            "content": ["<title>Google</title>"],
            "headers": {"Content-Type": "text/html; charset=ISO-8859-1"},
            "cookies": {"AEC": r".*"},
        },
        should_not_find={"content": ["groot"], "headers": {"nooooo": ""}, "cookies": {"nop": "a"}},
    )
