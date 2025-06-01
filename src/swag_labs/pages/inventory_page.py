#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Inventory page object model for swag-labs"""

import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from swag_labs.pages.page import Page

__all__ = (
    "InventoryPage",
    "InventoryItem",
)


class InventoryItem:
    """A class that represents an InventoryItem in the inventory page of the
    swag-labs website.

    Attributes
    ----------
        ITEM_NAME (tuple): the locator for the item name.
        ITEM_IMAGE (tuple): the locator for the item image.
        ITEM_DESCRIPTION (tuple): the locator for the item description.
        ITEM_PRICE (tuple): the locator for the item price.
        ADD_BUTTON (tuple): the locator for the add to cart button.
        ITEM_LINK (tuple): the locator for the item link.
        PRICE_REGEX (re.Pattern): a regular expression to parse the item
        price.
        ADD_BUTTON_TEXT (str): the text of the add to cart button.
        REMOVE_BUTTON_TEXT (str): the text of the remove from cart button.

    Methods
    -------
        name (): Returns the item's name as a string.
        description (): Returns the item's description as a string.
        link (): Returns the item's link as a clickable WebElement.
        image (): Returns the item's image as a clickable WebElement.
        price (): Returns the item's price as a float, parsed from the
        webpage text using a regular expression.
        in_cart (): Checks if the item is currently in the cart.
        add_to_cart (): Adds the item to the cart by clicking the "Add to
        cart" button.
        remove_from_cart (): Removes the item from the cart by clicking the
        "Remove from cart" button.

    """

    ITEM_NAME = (By.CSS_SELECTOR, "div.inventory_item_name")
    ITEM_IMAGE = (By.CSS_SELECTOR, "img.inventory_item_img")
    ITEM_DESCRIPTION = (By.CSS_SELECTOR, "div.inventory_item_desc")
    ITEM_PRICE = (By.CSS_SELECTOR, "div.inventory_item_price")
    ADD_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory")
    ITEM_LINK = (By.CSS_SELECTOR, "div.inventory_item_label > a")
    PRICE_REGEX = re.compile(r"\d+\.\d\d")
    ADD_BUTTON_TEXT = "Add to cart"
    REMOVE_BUTTON_TEXT = "Remove"

    def __init__(self, element: WebElement):
        self.element = element

    def _inventory_button(self) -> WebElement:
        return self.element.find_element(*self.ADD_BUTTON)

    def name(self) -> str:
        """get item's name"""
        return self.element.find_element(*self.ITEM_NAME).text.strip()

    def description(self) -> str:
        """get item's description"""
        return self.element.find_element(*self.ITEM_DESCRIPTION).text.strip()

    def link(self) -> WebElement:
        """get item's link as an web element that can be clicked"""
        return self.element.find_element(*self.ITEM_LINK)

    def image(self) -> WebElement:
        """get item's image as an web element that can be clicked"""
        return self.element.find_element(*self.ITEM_IMAGE)

    def price(self) -> float:
        """get item's price"""
        p = self.element.find_element(*self.ITEM_PRICE).text.strip()
        match = self.PRICE_REGEX.search(p)
        if match is None:
            raise NoSuchElementException("Couldn't parse item's price: " + p)
        return float(match.group())

    def in_cart(self) -> bool:
        """check if the item is in the cart"""
        return self._inventory_button().text.strip() == self.REMOVE_BUTTON_TEXT

    def add_to_cart(self) -> bool:
        """add the item to the cart"""
        if self.in_cart():
            return False
        self._inventory_button().click()
        return True

    def remove_from_cart(self) -> bool:
        """remove the item from the cart"""
        if not self.in_cart():
            return False
        self._inventory_button().click()
        return True

    def __str__(self):
        return self.name()


@Page.register_page_class(url="https://www.saucedemo.com/inventory.html")
class InventoryPage(Page):
    """A class that represents the inventory page of the swag-labs website

    Attributes
    ----------
        ITEM_CONTAINER (tuple): the locator for the item container
        CART_BUTTON (tuple): the locator for the cart button
        CART_COUNT (tuple): the locator for the cart count

    Methods
    -------
        items (): Returns a list of InventoryItem objects.
        check_cart (): Clicks the cart button.
        cart_count (): Returns the number of items in the cart.
        get_item_by_name (): Returns an InventoryItem object by name.

    """

    page_name = "home"
    url = "https://www.saucedemo.com/inventory.html"

    ITEM_CONTAINER = (By.CLASS_NAME, "inventory_item")
    CART_BUTTON = (By.CLASS_NAME, "shopping_cart_link")
    CART_COUNT = (By.CLASS_NAME, "shopping_cart_badge")
    BURGER_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        super().__init__(name=self.page_name, url=self.url, driver=driver)

    def _cart_button(self):
        return self.find_element(*self.CART_BUTTON)

    def _cart_count(self):
        return self.find_element(*self.CART_COUNT)

    def _side_bar_button(self):
        return self.find_element(*self.BURGER_BUTTON)

    def _logout_link(self):
        return self.find_element(*self.LOGOUT_LINK)

    def items(self):
        """returns a list of InventoryItem objects from the current page"""
        items = self.find_elements(*self.ITEM_CONTAINER)
        if not items:
            return []
        return (InventoryItem(item) for item in items)

    def check_cart(self) -> Page:
        """start checkout"""
        self._cart_button().click()
        return Page(
            name="cart",
            url="https://www.saucedemo.com/cart.html",
            driver=self.driver,
        )

    def cart_count(self) -> int:
        """returns the number of items in the cart"""
        try:
            return int(self._cart_count().text.strip())
        except NoSuchElementException:
            return 0

    def get_item_by_name(self, name: str) -> InventoryItem | None:
        """returns an InventoryItem object by its name"""
        for item in self.items():
            if item.name().lower() == name.strip().lower():
                return item
        return None

    def item_details_page(self, name: str) -> Page:
        """open item's details page by its name"""
        item = self.get_item_by_name(name)
        if item is not None:
            item.link().click()
            page_class = Page.get_page_class(self.driver.current_url)
            return page_class(self.driver)
        return self

    def add_item_to_cart(self, name: str) -> Page:
        """add an item to the cart by its name"""
        item = self.get_item_by_name(name)
        if item is not None:
            item.add_to_cart()
        return self

    def logout(self) -> Page:
        """logout from site"""
        self._side_bar_button().click()
        self._logout_link().click()
        page_class = Page.get_page_class(self.driver.current_url)
        return page_class(self.driver)
