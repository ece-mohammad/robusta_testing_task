#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""product details page object model for swag-labs"""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from swag_labs.pages.page import Page

__all__ = ("ProductPage",)


class ProductPage(Page):
    """product details page for swag-labs.

    Attributes
    ----------
        NAME (tuple): the locator for the product name.
        DESCRIPTION (tuple): the locator for the product description.
        PRICE (tuple): the locator for the product price.
        IMAGE (tuple): the locator for the product image.
        ADD_TO_CART_BUTTON (tuple): the locator for the add to cart button.
        ADD_TO_CART_BUTTON_TEXT (str): the text of the add to cart button.
        REMOVE_FROM_CART_BUTTON_TEXT (str): the text of the remove from cart
        button.
        BACK_BUTTON (tuple): the locator for the back button.
        BACK_BUTTON_TEXT (str): the text of the back button.
        CART_BUTTON (tuple): the locator for the cart button.
        CART_COUNT (tuple): the locator for the cart count.

    Methods
    -------
        item_name (): Returns the product's name as a string.
        description (): Returns the product's description as a string.
        link (): Returns the product's link as a clickable WebElement.
        image (): Returns the product's image as a clickable WebElement.
        price (): Returns the product's price as a float, parsed from the
        webpage text using a regular expression.
        in_cart (): Checks if the product is currently in the cart.
        add_to_cart (): Adds the product to the cart by clicking the "Add to
        cart" button.
        remove_from_cart (): Removes the product from the cart by clicking the
        "Remove from cart" button.
        back (): Clicks the back button.
        cart_count (): Returns the number of items in the cart.
        check_cart (): Clicks the cart button.

    """

    page_name = "product"
    url = "https://www.saucedemo.com/inventory-item.html"

    NAME = (By.CLASS_NAME, "inventory_details_name")
    DESCRIPTION = (By.CLASS_NAME, "inventory_details_desc")
    PRICE = (By.CLASS_NAME, "inventory_details_price")
    IMAGE = (By.CLASS_NAME, "inventory_details_img")
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart")
    ADD_TO_CART_BUTTON_TEXT = "Add to cart"
    REMOVE_FROM_CART_BUTTON_TEXT = "Remove"
    BACK_BUTTON = (By.CLASS_NAME, "inventory_details_back_button")
    BACK_BUTTON_TEXT = "Back to products"
    CART_BUTTON = (By.CLASS_NAME, "shopping_cart_link")
    CART_COUNT = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver: WebDriver):
        super().__init__(name=self.page_name, url=self.url, driver=driver)

    def _name(self) -> WebElement:
        return self.find_element(*self.NAME)

    def _description(self) -> WebElement:
        return self.find_element(*self.DESCRIPTION)

    def _price(self) -> WebElement:
        return self.find_element(*self.PRICE)

    def _image(self) -> WebElement:
        return self.find_element(*self.IMAGE)

    def _add_button(self) -> WebElement:
        return self.find_element(*self.ADD_TO_CART_BUTTON)

    def _back_button(self) -> WebElement:
        return self.find_element(*self.BACK_BUTTON)

    def _cart_button(self) -> WebElement:
        return self.find_element(*self.CART_BUTTON)

    def _cart_count(self) -> WebElement:
        return self.find_element(*self.CART_COUNT)

    def item_name(self) -> str:
        """get item's name"""
        return self._name().text.strip()

    def description(self) -> str:
        """get item's description"""
        return self._description().text.strip()

    def price(self) -> float:
        """get item's price"""
        return float(self._price().text.strip()[1:])

    def image(self) -> WebElement:
        """get item's image as an web element that can be clicked"""
        return self._image()

    def in_cart(self) -> bool:
        """check if the item is in the cart"""
        return (
            self._add_button().text.strip()
            == self.REMOVE_FROM_CART_BUTTON_TEXT
        )

    def add_to_cart(self) -> bool:
        """add the item to the cart"""
        if self.in_cart():
            return False
        self._add_button().click()
        return True

    def remove_from_cart(self) -> bool:
        """remove the item from the cart"""
        if not self.in_cart():
            return False
        self._add_button().click()
        return True

    def cart_count(self):
        """returns the number of items in the cart"""
        try:
            return int(self._cart_count().text.strip())
        except NoSuchElementException:
            return 0

    def back(self):
        """click the back button"""
        self._back_button().click()
        return Page(
            name="inventory",
            url="https://www.saucedemo.com/inventory.html",
            driver=self.driver,
        )

    def check_cart(self) -> Page:
        """check cart"""
        self._cart_button().click()
        return Page(
            name="cart",
            url="https://www.saucedemo.com/cart.html",
            driver=self.driver,
        )
