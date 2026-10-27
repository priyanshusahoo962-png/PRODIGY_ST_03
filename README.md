# PRODIGY_ST_03 

Automated login test suite for Sauce Demo, Prodigy InfoTech Software Testing Internship

**Tester:** Priyanshu Priyadarshi Sahoo

## Objective
Write an automated test suite that tests the login functionality of a web application, covering positive cases (valid credentials) and negative cases (invalid credentials, empty fields).

## Application Under Test
- **Website:** https://www.saucedemo.com/

## Tools Used
- Python 3
- Selenium WebDriver
- pytest
- Google Chrome

## Test Cases

| ID | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|
| TC_LOGIN_001 | Positive | Valid username and password | Products page opens | Pass |
| TC_LOGIN_002 | Positive | Logout after login | User returns to login page | Pass |
| TC_LOGIN_003 | Negative | Valid username, wrong password | Error message shown | Pass |
| TC_LOGIN_004 | Negative | Wrong username, valid password | Error message shown | Pass |
| TC_LOGIN_005 | Negative | Wrong username and password | Error message shown | Pass |
| TC_LOGIN_006 | Negative | Both fields empty | "Username is required" | Pass |
| TC_LOGIN_007 | Negative | Empty username | "Username is required" | Pass |
| TC_LOGIN_008 | Negative | Empty password | "Password is required" | Pass |
| TC_LOGIN_009 | Negative | Locked-out user | "User has been locked out" error | Pass |
| TC_LOGIN_010 | Negative | Password in wrong case | Error message shown | Pass |

## How to Run
1. Install Python and Google Chrome
2. Install the libraries: `python -m pip install selenium pytest`
3. Run the tests: `python -m pytest -v`

## Results
10 tests executed: 10 passed, 0 failed. 

## What I Learned
- How to automate browser actions with Selenium
- How to write positive and negative test cases
- How to use explicit waits to make tests reliable
- How to run and read pytest results
