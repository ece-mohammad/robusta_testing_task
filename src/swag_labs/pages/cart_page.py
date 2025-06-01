#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Cart page object model for swag-labs"""

import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from swag_labs.pages.page import Page

__all__ = ("CartPage", "CartItem")


class CartItem:
    """A class that represents an item in the cart.

    Attributes
    ----------
        NAME (tuple): the locator for the item name.
        DESCRIPTION (tuple): the locator for the item description.
        QUANTITY (tuple): the locator for the item quantity.
        PRICE (tuple): the locator for the item price.
        PRICE_PATTERN (re.Pattern): a regular expression to parse the item
        price.
        REMOVE_BUTTON (tuple): the locator for the remove button.

    Methods
    -------
        name (): Returns the item's name as a string.
        description (): Returns the item's description as a string.
        quantity (): Returns the item's quantity as an int.
        price (): Returns the item's price as a float, parsed from the
        webpage text using a regular expression.
        remove_item (): Removes the item from the cart by clicking the
        "Remove" button.

    """

    NAME = (By.CLASS_NAME, "inventory_item_name")
    DESCRIPTION = (By.CLASS_NAME, "inventory_item_desc")
    QUANTITY = (By.CLASS_NAME, "cart_quantity")
    PRICE = (By.CLASS_NAME, "inventory_item_price")
    REMOVE_BUTTON = (By.CLASS_NAME, "cart_button")
    PRICE_PATTERN = re.compile(r"\$(\d+\.\d+)")

    def __init__(self, element: WebElement):
        self.element: WebElement = element

    def _name(self):
        """get item's name"""
        return self.element.find_element(*self.NAME)

    def _description(self):
        return self.element.find_element(*self.DESCRIPTION)

    def _price(self):
        return self.element.find_element(*self.PRICE)

    def _quantity(self):
        return self.element.find_element(*self.QUANTITY)

    def _cancel_button(self):
        return self.element.find_element(*self.REMOVE_BUTTON)

    def name(self):
        """get item's name"""
        return self._name().text.strip()

    def description(self):
        """get item's description"""
        return self._description().text.strip()

    def price(self):
        """get item's price"""
        return float(self._price().text.strip()[1:])

    def quantity(self):
        """get item's quantity"""
        count = self._quantity().text.strip()
        match = self.PRICE_PATTERN.search(count)
        if match is None:
            raise NoSuchElementException("Couldn't parse quantity: " + count)
        return int(match.group(1))

    def remove_item(self):
        """remove the item from the cart"""
        self._cancel_button().click()


class CartPage(Page):
    """A class that represents cart page for swag-labs.

    Attributes
    ----------
        CART_ITEM_CONTAINER (tuple): the locator for the cart item container.
        BACK_BUTTON (tuple): the locator for the back button.
        CHECKOUT_BUTTON (tuple): the locator for the checkout button.

    Methods
    -------
        items (): Returns a list of CartItem objects.
        count_items (): Returns the number of unique items in the cart.
        total_items (): Returns the total number of items in the cart.
        total_price (): Returns the total price of the items in the cart.
        clear_cart (): Removes all items from the cart.
        remove_item (): Removes an item from the cart.
        go_back (): Returns the inventory page by clicking the back button.
        goto_checkout (): Returns the checkout overview page by clicking the
        checkout button.



    """

    page_name = "cart"
    url = "https://www.saucedemo.com/cart.html"

    CART_ITEM_CONTAINER = (By.CLASS_NAME, "cart_item")
    BACK_BUTTON = (By.CLASS_NAME, "back")
    CHECKOUT_BUTTON = (By.CLASS_NAME, "checkout-button")

    def __init__(self, driver: WebDriver):
        super().__init__(name=self.page_name, url=self.url, driver=driver)

    def _items_container(self):
        return self.find_elements(*self.CART_ITEM_CONTAINER)

    def _back_button(self):
        return self.find_element(*self.BACK_BUTTON)

    def _checkout_button(self):
        return self.find_element(*self.CHECKOUT_BUTTON)

    def items(self):
        """get items in cart"""
        return (CartItem(element) for element in self._items_container())

    def count_items(self):
        """get number of unique items in cart"""
        return len(self._items_container())

    def total_items(self):
        """get total number of items in cart"""
        return sum(item.quantity() for item in self.items())

    def total_price(self):
        """get total price of items in cart"""
        return sum(item.price() * item.quantity() for item in self.items())

    def clear_cart(self):
        """remove all items from cart"""
        for item in self.items():
            item.remove_item()
        return self

    def remove_item(self, name: str):
        """remove an item from the cart"""
        for item in self.items():
            if item.name().lower() == name.strip().lower():
                item.remove_item()
        return self

    def go_back(self):
        """go back to inventory"""
        self._back_button().click()
        return Page(
            name="inventory",
            url="https://www.saucedemo.com/inventory.html",
            driver=self.driver,
        )

    def goto_checkout(self):
        """go to checkout"""
        self._checkout_button().click()
        return Page(
            name="checkout_info",
            url="https://www.saucedemo.com/checkout-step-one.html",
            driver=self.driver,
        )
