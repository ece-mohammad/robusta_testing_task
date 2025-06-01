"""Test user login"""

import pytest

from swag_labs.pages.inventory_page import InventoryPage
from swag_labs.pages.login import LoginPage


class TestLogin:
    def test_correct_credentials_expect_inventory_page(
        self, driver, username, password
    ):
        login = LoginPage(driver)
        login.open()
        new_page = login.login(username, password)
        assert new_page.url == InventoryPage.url
        assert new_page.page_name == InventoryPage.page_name
        assert isinstance(new_page, InventoryPage)
        new_page.logout()

    def test_missing_username_expect_error_message(self, driver, password):
        login = LoginPage(driver)
        login.open()
        login.login("", password)
        assert login.error_message() == "Epic sadface: Username is required"

    def test_missing_password_expect_error_message(self, driver, username):
        login = LoginPage(driver)
        login.open()
        login.login(username, "")
        assert login.error_message() == "Epic sadface: Password is required"

    def test_wrong_username_expect_error_message(self, driver, password):
        login = LoginPage(driver)
        login.open()
        login.login("wrong_username", password)
        assert login.error_message() == (
            "Epic sadface: Username and password do not match any user in this service"
        )

    def test_wrong_password_expect_error_message(self, driver, username):
        login = LoginPage(driver)
        login.open()
        login.login(username, "wrong_password")
        assert login.error_message() == (
            "Epic sadface: Username and password do not match any user in this service"
        )
