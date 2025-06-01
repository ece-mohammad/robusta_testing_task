#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Login page object model for swag-labs"""

from typing import Self

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from swag_labs.pages.page import Page

__all__ = ("LoginPage",)


@Page.register_page_class(url="https://www.saucedemo.com/")
class LoginPage(Page):
    """LoginPage class, provides methods to interact with the login page of
    swag-labs.

    Attributes
    ----------
        USERNAME_INPUT (tuple): the locator for the username input field
        PASSWORD_INPUT (tuple): the locator for the password input field
        LOGIN_BUTTON (tuple): the locator for the login button

    Methods
    -------
        enter_user_name (username: str): enter the username in the username
        input field.
        enter_password (password: str): enter the password in the password
        input field.
        click_login (): click the login button.
        get_error_message (): get the error message (if any).
        login (username: str, password: str): login to the swag-labs website
        with given credentials.
    """

    page_name = "login"
    url = "https://www.saucedemo.com/"

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message-container")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(name=self.page_name, url=self.url, driver=driver)

    def open(self):
        super().open()
        WebDriverWait(
            self.driver,
            10,
            poll_frequency=0.5,
        ).until(EC.presence_of_element_located(self.LOGIN_BUTTON))

    def _username_input(self) -> WebElement:
        return self.find_element(*self.USERNAME_INPUT)

    def _password_input(self) -> WebElement:
        return self.find_element(*self.PASSWORD_INPUT)

    def _error_container(self) -> WebElement:
        return self.find_element(*self.ERROR_MESSAGE)

    def _login_button(self) -> WebElement:
        return self.find_element(*self.LOGIN_BUTTON)

    def _enter_user_name(self, username: str) -> Self:
        self._username_input().click()
        self._username_input().clear()
        self._username_input().send_keys(username)
        return self

    def _enter_password(self, password: str) -> Self:
        self._password_input().click()
        self._password_input().clear()
        self._password_input().send_keys(password)
        return self

    def _click_login(self) -> Self:
        self._login_button().click()
        return self

    def error_message(self) -> str:
        """get the error message (if any)"""
        try:
            return self._error_container().text.strip()
        except NoSuchElementException:
            return ""

    def login(self, username: str, password: str) -> Page:
        """login using the given credentials"""
        self._enter_user_name(username)
        self._enter_password(password)
        self._click_login()
        page_class = Page.get_page_class(self.driver.current_url)
        return page_class(self.driver)
