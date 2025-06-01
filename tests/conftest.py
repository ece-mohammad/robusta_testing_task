#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""pytest fixtures for swag-labs website tests"""

import pytest
from environs import env
from selenium.webdriver.remote.webdriver import WebDriver

from tests.utils.driver import get_chrome_driver, get_firefox_driver

env.read_env(".env.test")


@pytest.fixture(scope="session")
def setup():
    """fixture to setup a new driver instance for test session"""

    browser = env.str("BROWSER", default="chrome")

    # chrome
    if browser == "chrome":
        browser = get_chrome_driver(headless=True)

    # firefox
    elif browser == "firefox":
        browser = get_firefox_driver(headless=True)

    else:
        raise ValueError(f"Browser {browser} is not supported")

    browser.maximize_window()
    browser.implicitly_wait(10)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def driver(request, setup: WebDriver):
    """Fixture to clean browser state before each test function."""
    # Clear cookies and storage to ensure clean state
    setup.get("about:blank")
    request.cls.driver = setup
    yield
    setup.delete_all_cookies()
    setup.execute_script("window.sessionStorage.clear();")
    setup.execute_script("window.localStorage.clear();")


@pytest.fixture(scope="session")
def username() -> str:
    """get login username"""
    return "standard_user"


@pytest.fixture(scope="session")
def password() -> str:
    """get login password"""
    return "secret_sauce"
