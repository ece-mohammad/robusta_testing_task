#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Checkout info (checkout step 1) page object model for swag-labs"""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from swag_labs.pages.page import Page

__all__ = ("CheckoutInfoPage",)


@Page.register_page_class("https://www.saucedemo.com/checkout-step-one.html")
class CheckoutInfoPage(Page):
    """A class that represents the checkout info page for swag-labs.

    Attributes
    ----------
        FIRST_NAME_INPUT (tuple): the locator for the first name input.
        LAST_NAME_INPUT (tuple): the locator for the last name input.
        POSTAL_CODE_INPUT (tuple): the locator for the postal code input.
        CONTINUE_BUTTON (tuple): the locator for the continue button.
        CANCEL_BUTTON (tuple): the locator for the cancel button.
        ERROR_MESSAGE (tuple): the locator for the error message.

    Methods
    -------
        enter_first_name (first_name: str): enter the first name.
        enter_last_name (last_name: str): enter the last name.
        enter_postal_code (postal_code: str): enter the postal code.
        click_continue (): click the continue button.
        click_cancel (): click the cancel button.
        get_error_message (): get the error message.
        continue_checkout (): continue to the checkout overview page.
        cancel_checkout (): cancel checkout.

    """

    page_name = "checkout_info"
    url = "https://www.saucedemo.com/checkout-step-one.html"

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message-container")

    def __init__(self, driver):
        super().__init__(name=self.page_name, url=self.url, driver=driver)

    def open(self):
        super().open()
        WebDriverWait(
            self.driver,
            10,
            poll_frequency=0.5,
        ).until(EC.presence_of_element_located(self.CONTINUE_BUTTON))

    def _first_name(self) -> WebElement:
        return self.find_element(*self.FIRST_NAME_INPUT)

    def _last_name(self) -> WebElement:
        return self.find_element(*self.LAST_NAME_INPUT)

    def _postal_code(self) -> WebElement:
        return self.find_element(*self.POSTAL_CODE_INPUT)

    def _continue_button(self) -> WebElement:
        return self.find_element(*self.CONTINUE_BUTTON)

    def _cancel_button(self) -> WebElement:
        return self.find_element(*self.CANCEL_BUTTON)

    def _error_message(self) -> WebElement:
        return self.find_element(*self.ERROR_MESSAGE)

    def enter_first_name(self, first_name: str):
        """enter user's first name"""
        self._first_name().send_keys(first_name)
        return self

    def enter_last_name(self, last_name: str):
        """enter user's last name"""
        self._last_name().send_keys(last_name)
        return self

    def enter_postal_code(self, postal_code: str):
        """enter user's postal code"""
        self._postal_code().send_keys(postal_code)
        return self

    def enter_user_info(
        self, first_name: str, last_name: str, postal_code: str
    ):
        """enter user's information for checkout"""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self

    def error_message(self) -> str:
        """get the error message (if any)"""
        try:
            return self._error_message().text.strip()
        except NoSuchElementException:
            return ""

    def continue_checkout(self):
        """continue checkout"""
        self._continue_button().click()
        if self.driver.current_url == self.url:
            return self

        page_class = Page.get_page_class(self.driver.current_url)
        return page_class(self.driver)

    def cancel_checkout(self):
        """cancel checkout"""
        self._cancel_button().click()
        page_class = Page.get_page_class(self.driver.current_url)
        return page_class(self.driver)
