#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Testing a user journey on the e-commerce website SauceDemo.
This test focuses on core functionalities such as logging in,
adding products to the cart, verifying the contents, and completing a
purchase using data from an external API.
"""

from urllib.parse import urlparse

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
    def test_user_journey(self, driver, username, password, user_info):
        # open login page ----------------------------------------------------
        login_page = LoginPage(driver)
        login_page.open()
        assert login_page.driver.current_url == LoginPage.url

        # login --------------------------------------------------------------
        inventory: InventoryPage = login_page.login(username, password)

        # check successful login
        assert inventory.driver.current_url == InventoryPage.url
        assert inventory.title() == "Products"

        # check that the cart is empty
        cart_items = inventory.cart_count()
        assert cart_items == 0

        # get first item from products page ----------------------------------
        fleece_jacket: InventoryItem | None = inventory.get_item_by_name(ITEM1)

        # check item is found in page
        assert fleece_jacket is not None

        # add first item to cart ---------------------------------------------
        jacket_price = fleece_jacket.price()
        jacket_name = fleece_jacket.name()

        # check item name
        assert fleece_jacket.name() == ITEM1

        # add to cart & check cart is incremented by 1
        fleece_jacket.add_to_cart()
        assert inventory.cart_count() == 1

        # open second item details page --------------------------------------
        onsie_page: ProductPage = inventory.item_details_page(ITEM2)
        assert compare_urls(onsie_page.driver.current_url, ProductPage.url)

        # second item data
        onsie_name = onsie_page.item_name()
        onsie_price = onsie_page.price()
        assert onsie_name == ITEM2

        # add second item to cart & check cart is incremented by 1
        onsie_page.add_to_cart()
        assert onsie_page.cart_count() == 2

        # get to cart details page -------------------------------------------
        cart_page: CartPage = onsie_page.check_cart()
        assert cart_page.driver.current_url == CartPage.url
        assert cart_page.count_items() == 2

        # verify item1
        cart_item1 = cart_page.get_item(jacket_name)
        assert cart_item1 is not None
        assert cart_item1.name() == jacket_name
        assert cart_item1.price() == jacket_price

        # verify item2
        cart_item2 = cart_page.get_item(onsie_name)
        assert cart_item2 is not None
        assert cart_item2.name() == onsie_name
        assert cart_item2.price() == onsie_price

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
