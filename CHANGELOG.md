# Changelog
## 0.8.0 (Unreleased)
- chore: update dependencies
- feat: improve assert report
- feat: add attribute history on PageChecker

## 0.7.0
- feat: possible to pass string when check content
- chore: update dependencies
- chore: add py.typed file

## 0.6.0
- BREAKING CHANGE: remove HttpClientConfiguration
- chore: update dependencies
- refactor: internal classes

## 0.5.0
- chore: update dependencies
- feat: possible to pass str base_url in PageChecker

## 0.4.0
- chore: update dependencies
- chore: export public members from package level
- chore: use ABC instead of Protocol for Validator class
- chore: improve message when assert failed

## 0.3.1
- chore: update dependencies
- chore: add deprecated warning on "http_client_config" fixture

## 0.3.0
- feat: pass kwargs from PageChecker call to httpx request
- feat: add property `previous_response` on PageChecker
- chore: update dependencies

## 0.2.0
- Add validators: Regex and Text
- Rename Cookie.value_pattern to Cookie.value
