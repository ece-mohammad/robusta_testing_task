#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Testing a user journey on the e-commerce website SauceDemo.
This test focuses on core functionalities such as logging in,
adding products to the cart, verifying the contents, and completing a
purchase using data from an external API.
"""

from urllib.parse import urlparse

from swag_labs.pages import item_page
from swag_labs.pages.cart_page import CartItem, CartPage
from swag_labs.pages.checkout_complete import CheckoutCompletePage
from swag_labs.pages.checkout_info import CheckoutInfoPage
from swag_labs.pages.checkout_overview import CheckoutOverviewPage
from swag_labs.pages.inventory_page import InventoryItem, InventoryPage
from swag_labs.pages.login import LoginPage
from swag_labs.pages.product_page import ProductPage

ITEM1 = "Sauce Labs Fleece Jacket"
ITEM2 = "Sauce Labs Onesie"


def compare_urls(url1: str, url2: str):
    u1 = urlparse(url1)
    u2 = urlparse(url2)
    return (
        u1.scheme == u2.scheme
        and u1.netloc == u2.netloc
        and u1.path == u2.path
    )


class TestUerJourney:
    def user_login(self, driver, username, password):
        # open login page
        login_page = LoginPage(driver)
        login_page.open()
        assert login_page.driver.current_url == LoginPage.url
        inventory: InventoryPage = login_page.login(username, password)

        # check successful login
        assert inventory.driver.current_url == InventoryPage.url
        assert inventory.title() == "Products"

        return inventory

    def add_item_to_cart(self, page: InventoryPage, item_name):
        # get first item from products page ----------------------------------
        item: InventoryItem | None = page.get_item_by_name(ITEM1)
        assert item is not None
        assert item.name() == item_name

        # add to cart & check cart is incremented by 1
        count = page.cart_count()
        item.add_to_cart()
        assert page.cart_count() == count + 1

        return page

    def open_item_details(self, page: InventoryPage, item_name):
        item_page: ProductPage = page.item_details_page(item_name)
        count = item_page.cart_count()

        assert item_page.item_name() == item_name
        assert item_page.add_to_cart()
        assert item_page.cart_count() == count + 1
        return item_page

    def open_and_verify_cart(self, page: ProductPage, items):
        cart_page: CartPage = page.check_cart()
        for item in items:
            cart_item = cart_page.get_item(item[0])
            assert cart_item is not None
            assert cart_item.name() == item[0]
            assert cart_item.price() == item[1]

        return cart_page

    def test_user_journey(self, driver, username, password, user_info):
        # login and goto products page
        products_page = self.user_login(driver, username, password)

        # get items data from the products page
        jacket_name = products_page.get_item_by_name(ITEM1).name()
        jacket_price = products_page.get_item_by_name(ITEM1).price()
        onsie_name = products_page.get_item_by_name(ITEM2).name()
        onsie_price = products_page.get_item_by_name(ITEM2).price()

        # add first item to cart (jacket)
        self.add_item_to_cart(products_page, ITEM1)

        # open second item details page & add it to cart (onsie)
        onsie_details_page = self.open_item_details(products_page, ITEM2)

        # open cart & verify items
        cart_page = self.open_and_verify_cart(
            onsie_details_page,
            (
                (ITEM1, jacket_price),
                (ITEM2, onsie_price),
            ),
        )

        # get to checkout info page ------------------------------------------
        checkout_info: CheckoutInfoPage = cart_page.goto_checkout()

        checkout_info.enter_user_info(
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            postal_code=user_info["zip"],
        )
        checkout_overview: CheckoutOverviewPage = (
            checkout_info.continue_checkout()
        )
        # check that info is accepted
        assert checkout_overview.driver.current_url == CheckoutOverviewPage.url

        # get to checkout overview page --------------------------------------
        co_jacket: CartItem = checkout_overview.get_item(jacket_name)
        assert co_jacket is not None
        assert co_jacket.name() == jacket_name
        assert co_jacket.price() == jacket_price
        assert co_jacket.quantity() == 1

        co_onsie: CartItem = checkout_overview.get_item(onsie_name)
        assert co_onsie is not None
        assert co_onsie.name() == onsie_name
        assert co_onsie.price() == onsie_price
        assert co_onsie.quantity() == 1

        # check price
        tax = checkout_overview.tax()
        assert (
            abs(
                (jacket_price + onsie_price)
                - checkout_overview.price_before_tax()
            )
            < 1e-3
        )
        assert (
            abs(
                (tax + jacket_price + onsie_price)
                - checkout_overview.price_after_tax()
            )
            < 1e-3
        )

        # complete checkout -------------------------------------------------
        checkout_complete: CheckoutCompletePage = (
            checkout_overview.finish_checkout()
        )
        assert checkout_complete.driver.current_url == CheckoutCompletePage.url
