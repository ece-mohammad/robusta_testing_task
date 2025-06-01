#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Base POM (Page Object Model) class for swag-labs pages"""

from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

__all__ = ("Page",)


class Page:
    """Base page class, provides common page methods and variables.

    Attributes
    -----------
        name (str): name of the page
        url (str): url of the page
        driver (WebDriver): selenium driver used to interact with the page

    Methods
    --------
        - open(): open the page
        - is_open(): check if the page is open
        - find_element(): find an element on the page
        - find_elements(): find multiple elements on the page
    """

    TITLE = (By.CLASS_NAME, "title")

    def __init__(
        self, name: str, url: str, driver: WebDriver, auto_open: bool = False
    ):
        self.page_name: str = name
        self.url: str = url
        self.driver: WebDriver = driver
        if auto_open and not self.is_open():
            self.open()

    def title(self) -> str:
        """get the title of the page"""
        try:
            title = self.driver.find_element(*self.TITLE).text.strip()
        except NoSuchElementException:
            title = self.driver.title
        return title

    def open(self):
        """open the page's url in the browser"""
        self.driver.get(self.url)

    def is_open(self) -> bool:
        """check if the page is currently open in the browser"""
        return self.driver.current_url == self.url

    def find_element(
        self, by: str, value: str, wait: int = 0, poll_frequency: float = 0.5
    ) -> WebElement:
        """find a single element on the page"""
        if wait > 0:
            return WebDriverWait(
                self.driver, wait, poll_frequency=poll_frequency
            ).until(EC.presence_of_element_located((by, value)))
        else:
            return self.driver.find_element(by, value)

    def find_elements(
        self, by: str, value: str, wait: int = 0, poll_frequency: float = 0.5
    ) -> List[WebElement]:
        """find multiple elements on the page"""
        if wait > 0:
            return WebDriverWait(
                self.driver, wait, poll_frequency=poll_frequency
            ).until(EC.presence_of_all_elements_located((by, value)))
        else:
            return self.driver.find_elements(by, value)

    def __str__(self):
        return f"{self.page_name}: {self.title()}"


# TODO register pages in page class
# TODO get pages by url and path
