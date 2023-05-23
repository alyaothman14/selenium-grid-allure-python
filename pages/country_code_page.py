"""
This defines the login page components
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import Union, Tuple
from selenium.webdriver import Chrome, Firefox
import allure


class SportyCountryCodePage(BasePage):

    MOBILE_NUMBER: Tuple[By, str] = (
        By.XPATH, "//input[@placeholder='Mobile Number']")
    START_EXPLORING: Tuple[By, str] = (
        By.XPATH, "//button[span='Start Exploring']")
    PASSWORD: Tuple[By, str] = (By.XPATH, "//input[@placeholder='Password']")
    LOGIN_BUTTON: Tuple[By, str] = (By.XPATH, "//button[span='Log In']")
    COUNTRY_CODE: Tuple[By, str] = (
        By.XPATH, "//div[contains(@class, 'phone-input')]")

    def __init__(self, driver: Union[Chrome, Firefox]):
        super().__init__(driver)

    @allure.step("User select country")
    def click_country_code(self, country_name: str):
        country_name_xpath: Tuple[By, str] = (
            By.XPATH, "//*[contains(text(),'%s')]" % country_name)
        self.click(country_name_xpath)
