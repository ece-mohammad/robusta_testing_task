#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Checkout complete page object model for swag-labs"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from swag_labs.pages.page import Page

__all__ = ("CheckoutCompletePage",)


@Page.register_page_class("https://www.saucedemo.com/checkout-complete.html")
class CheckoutCompletePage(Page):
    """A class that represents the checkout complete page for swag-labs.

    Attributes
    ----------
        CONTINUE_BUTTON (tuple): the locator for the continue button.

    Methods
    -------
        back (): Returns the inventory page by clicking the continue button.
    """

    page_name = "checkout_complete"
    url = "https://www.saucedemo.com/checkout-complete.html"
    CONTINUE_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver: WebDriver):
        super().__init__(name=self.page_name, url=self.url, driver=driver)

    def open(self):
        super().open()
        WebDriverWait(
            self.driver,
            10,
            poll_frequency=0.5,
        ).until(EC.presence_of_element_located(self.CONTINUE_BUTTON))

    def _back_button(self) -> WebElement:
        return self.find_element(*self.CONTINUE_BUTTON)

    def back(self):
        """click the back button"""
        self._back_button().click()
        page_class = Page.get_page_class(self.driver.current_url)
        return page_class(self.driver)
