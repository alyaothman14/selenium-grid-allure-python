from typing import Union
from pages.country_code_page import SportyCountryCodePage
from pages.login_page import SportyLoginPage
from selenium.webdriver import Chrome, Firefox
import pytest


from pages.nav_bar_page import SportyNavBarPage


@pytest.mark.usefixtures("setup")
class BaseTest:
    driver: Union[Chrome, Firefox]
    login_page: SportyLoginPage
    nav_bar: SportyNavBarPage
    country_code: SportyCountryCodePage
    browser: str
