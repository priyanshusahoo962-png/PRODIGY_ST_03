
"""
PRODIGY_ST_03 - Automated Login Tests for https://www.saucedemo.com/
Tools: Python, Selenium, pytest
Run with: pytest -v
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.saucedemo.com/"
VALID_USER = "standard_user"
LOCKED_USER = "locked_out_user"
VALID_PASSWORD = "secret_sauce"


@pytest.fixture
def driver():
    """Open a fresh Chrome browser before each test and close it after."""
    options = webdriver.ChromeOptions()
    # Turn off Chrome's password pop-ups, which can block clicks during tests
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_argument("--disable-notifications")
    drv = webdriver.Chrome(options=options)
    drv.maximize_window()
    drv.get(URL)
    yield drv
    drv.quit()


def login(driver, username, password):
    """Type the username and password and click the Login button."""
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


def get_error_text(driver):
    """Wait for the red error box and return its text."""
    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )
    return error.text


# ---------------- POSITIVE TEST CASES ----------------

def test_valid_login(driver):
    """TC_LOGIN_001: Valid username and password should open the Products page."""
    login(driver, VALID_USER, VALID_PASSWORD)
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    assert "inventory.html" in driver.current_url
    assert driver.find_element(By.CSS_SELECTOR, ".title").text == "Products"


def test_logout_after_login(driver):
    """TC_LOGIN_002: User should be able to log out and return to the login page."""
    wait = WebDriverWait(driver, 15)
    login(driver, VALID_USER, VALID_PASSWORD)
    wait.until(EC.url_contains("inventory.html"))
    wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "login-button")))
    assert driver.current_url.rstrip("/") == URL.rstrip("/")


# ---------------- NEGATIVE TEST CASES ----------------

def test_invalid_password(driver):
    """TC_LOGIN_003: Valid username with wrong password should show an error."""
    login(driver, VALID_USER, "wrong_password")
    assert "Username and password do not match" in get_error_text(driver)


def test_invalid_username(driver):
    """TC_LOGIN_004: Wrong username with valid password should show an error."""
    login(driver, "wrong_user", VALID_PASSWORD)
    assert "Username and password do not match" in get_error_text(driver)


def test_invalid_username_and_password(driver):
    """TC_LOGIN_005: Wrong username and wrong password should show an error."""
    login(driver, "wrong_user", "wrong_password")
    assert "Username and password do not match" in get_error_text(driver)


def test_empty_username_and_password(driver):
    """TC_LOGIN_006: Both fields empty should show 'Username is required'."""
    login(driver, "", "")
    assert "Username is required" in get_error_text(driver)


def test_empty_username(driver):
    """TC_LOGIN_007: Empty username with a password should show 'Username is required'."""
    login(driver, "", VALID_PASSWORD)
    assert "Username is required" in get_error_text(driver)


def test_empty_password(driver):
    """TC_LOGIN_008: Username with empty password should show 'Password is required'."""
    login(driver, VALID_USER, "")
    assert "Password is required" in get_error_text(driver)


def test_locked_out_user(driver):
    """TC_LOGIN_009: A locked-out user should not be able to log in."""
    login(driver, LOCKED_USER, VALID_PASSWORD)
    assert "locked out" in get_error_text(driver)


def test_password_is_case_sensitive(driver):
    """TC_LOGIN_010: Password in the wrong case should be rejected."""
    login(driver, VALID_USER, "SECRET_SAUCE")
    assert "Username and password do not match" in get_error_text(driver)
