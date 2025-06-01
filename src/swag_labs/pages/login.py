#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Login page object model for swag-labs"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from swag_labs.pages.inventory_page import InventoryPage
from swag_labs.pages.page import Page

__all__ = ("LoginPage",)


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

    def __init__(self, driver: WebDriver):
        super().__init__(name=self.page_name, url=self.url, driver=driver)

    def _username_input(self):
        return self.find_element(*self.USERNAME_INPUT)

    def _password_input(self):
        return self.find_element(*self.PASSWORD_INPUT)

    def _error_container(self):
        return self.find_element(*self.ERROR_MESSAGE)

    def _login_button(self):
        return self.find_element(*self.LOGIN_BUTTON)

    def _enter_user_name(self, username: str) -> Page:
        self._username_input().click()
        self._username_input().clear()
        self._username_input().send_keys(username)
        return self

    def _enter_password(self, password: str) -> Page:
        self._password_input().click()
        self._password_input().clear()
        self._password_input().send_keys(password)
        return self

    def _click_login(self) -> Page:
        self._login_button().click()
        return self

    def error_message(self) -> str:
        """get the error message (if any)"""
        return self._error_container().text.strip()

    def login(self, username: str, password: str) -> Page:
        """login using the given credentials"""
        self._enter_user_name(username)
        self._enter_password(password)
        self._click_login()

        if self.driver.current_url == InventoryPage.url:
            return InventoryPage(self.driver)

        return self


# TODO remove
if __name__ == "__main__":
    from swag_labs.utils.driver import get_chrome_driver

    browser = get_chrome_driver(headless=False)
    login = LoginPage(browser)
    login.open()
    login.login("standard_user", "secret_sauce")
    input()
    browser.quit()
