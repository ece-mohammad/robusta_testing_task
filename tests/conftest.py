#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""pytest fixtures for swag-labs website tests"""

import json
from urllib.request import Request, urlopen

import pytest
from environs import env
from selenium.webdriver.remote.webdriver import WebDriver

from tests.utils.driver import get_chrome_driver, get_firefox_driver

env.read_env(".env.test")

DATA_END_POINT = env.str(
    "DATA_END_POINT",
    default="https://my-json-server.typicode.com/ece-mohammad/fake_json_server_store/users/1",
)


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


# pylint: disable=redefined-outer-name
@pytest.fixture(scope="function")
def driver(setup: WebDriver):
    """Fixture to clean browser state before each test function."""
    # Clear cookies and storage to ensure clean state
    setup.get("about:blank")
    yield setup
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


@pytest.fixture(scope="session")
def user_info():
    request = Request(DATA_END_POINT)
    return json.loads(urlopen(request).read().decode("utf-8"))
