#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options as FFoxOptions
from selenium.webdriver.firefox.service import Service as FFoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def get_chrome_driver(headless=True):
    """get a new chrome webdriver driver instance"""

    options = ChromeOptions()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    options.add_argument("--disable-notifications")
    options.add_experimental_option(
        "prefs",
        {
            "profile.managed_default_content_settings.images": 2,
        },
    )
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_firefox_driver(headless=True):
    """get a new firefox webdriver instance"""

    options = FFoxOptions()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    options.add_argument("--private-window")
    options.add_argument("--disable-notifications")
    profile = FirefoxProfile()
    profile.set_preference("permissions.default.image", 2)
    options.profile = profile
    service = FFoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    return driver
