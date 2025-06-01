#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Checkout overview (checkout step 2) page object model for swag-labs"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from swag_labs.pages.cart_page import CartItem
from swag_labs.pages.page import Page

__all__ = ("CheckoutOverviewPage",)


class CheckoutOverviewPage(Page):
    """A class that represents the checkout overview page (checkout step 2)
    for swag-labs.

    Attributes
    ----------
        CART_ITEM_CONTAINER (tuple): the locator for the cart item container.
        CANCEL_BUTTON (tuple): the locator for the cancel button.
        FINISH_BUTTON (tuple): the locator for the finish button.
        PAYMENT_INFO (tuple): the locator for the payment info.
        SHIPPING_INFO (tuple): the locator for the shipping info.
        SUBTOTAL (tuple): the locator for the subtotal.
        TAX (tuple): the locator for the tax.
        TOTAL (tuple): the locator for the total.

    Methods
    -------
        items (): Returns a list of CartItem objects.
        get_item (): Returns a CartItem object by name.
        payment_info (): Returns the payment info as a string.
        shipping_info (): Returns the shipping info as a string.
        price_before_tax (): Returns the subtotal as a float.
        tax (): Returns the tax as a float.
        price_after_tax (): Returns the total as a float.
        cancel (): Returns the inventory page by clicking the cancel button.
        finish (): Returns the checkout complete page by clicking the finish
        button.

    """

    page_name = "checkout_overview"
    url = "https://www.saucedemo.com/checkout-step-two.html"

    CART_ITEM_CONTAINER = (By.CLASS_NAME, "cart_item")
    CANCEL_BUTTON = (By.ID, "cancel")
    FINISH_BUTTON = (By.ID, "finish")
    PAYMENT_INFO = (By.CSS_SELECTOR, "[data-test='payment-info-value']")
    SHIPPING_INFO = (By.CSS_SELECTOR, "[data-test='shipping-info-value']")
    SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")

    def __init__(self, driver):
        super().__init__(name=self.page_name, url=self.url, driver=driver)

    def _finish_button(self) -> WebElement:
        return self.find_element(*self.FINISH_BUTTON)

    def _cancel_button(self) -> WebElement:
        return self.find_element(*self.CANCEL_BUTTON)

    def _cart_item_container(self):
        return self.find_elements(*self.CART_ITEM_CONTAINER)

    def _payment_info(self) -> WebElement:
        return self.find_element(*self.PAYMENT_INFO)

    def _shipping_info(self) -> WebElement:
        return self.find_element(*self.SHIPPING_INFO)

    def _price_subtotal(self) -> WebElement:
        return self.find_element(*self.SUBTOTAL)

    def _tax(self) -> WebElement:
        return self.find_element(*self.TAX)

    def _total(self) -> WebElement:
        return self.find_element(*self.TOTAL)

    def items(self):
        """get items in cart"""
        return (CartItem(item) for item in self._cart_item_container())

    def get_item(self, name: str):
        """get item by name"""
        for item in self.items():
            if item.name() == name:
                return item
        return None

    def payment_info(self) -> str:
        """get payment info"""
        return self._payment_info().text

    def shipping_info(self) -> str:
        """get shipping info"""
        return self._shipping_info().text

    def price_before_tax(self) -> float:
        """get price before tax"""
        text = self._price_subtotal().text.strip()
        return float(text[text.find("$") + 1 :])

    def tax(self) -> float:
        """get tax"""
        text = self._tax().text.strip()
        return float(text[text.find("$") + 1 :])

    def price_after_tax(self) -> float:
        """get total price (item total + tax)"""
        text = self._total().text.strip()
        return float(text[text.find("$") + 1 :])

    def cancel_checkout(self):
        """cancel checkout"""
        self._cancel_button().click()
        return Page(
            "Inventory",
            "https://www.saucedemo.com/inventory.html",
            self.driver,
        )

    def finish_checkout(self):
        """finish checkout"""
        self._finish_button().click()
        return Page(
            name="checkout_complete",
            url="https://www.saucedemo.com/checkout-complete.html",
            driver=self.driver,
        )
