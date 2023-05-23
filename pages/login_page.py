"""
This defines the login page components
"""
from selenium.webdriver.common.by import By
from pages.nav_bar_page import SportyNavBarPage
from typing import Union, Tuple
from selenium.webdriver import Chrome, Firefox
import allure


class SportyLoginPage(SportyNavBarPage):

    MOBILE_NUMBER: Tuple[By, str] = (
        By.XPATH, "//input[@placeholder='Mobile Number']")
    START_EXPLORING: Tuple[By, str] = (
        By.XPATH, "//button[span='Start Exploring']")
    PASSWORD: Tuple[By, str] = (By.XPATH, "//input[@placeholder='Password']")
    LOGIN_BUTTON: Tuple[By, str] = (By.XPATH, "//button[span='Log In']")
    COUNTRY_CODE_COMBOBOX: Tuple[By, str] = (
        By.XPATH, "//div[contains(@class, 'phone-input')]//i")
    COUNTRY_CODE: Tuple[By, str] = (
        By.XPATH, "//div[contains(@class, 'phone-input')]//div[contains(@class, 'phone')]")
    COUNTRY_FLAG: Tuple[By, str] = (
        By.XPATH, "//div[contains(@class, 'phone-input')]//img[contains(@class, 'flag')]")

    def __init__(self, driver: Union[Chrome, Firefox]):
        super().__init__(driver)

    @allure.step("Fill phone number")
    def fill_phone_number(self, phone_number: str) -> None:
        self.fill_text(self.MOBILE_NUMBER, phone_number)

    @allure.step("User clicks start exploring")
    def click_start_exploring(self) -> None:
        self.click(self.START_EXPLORING)

    @allure.step("User fills verification code")
    def fill_verification_code(self, code):
        pass

    @allure.step("User fill password")
    def fill_password(self, password: str) -> None:
        self.fill_text(self.PASSWORD, password)

    @allure.step("User clicks login button")
    def click_login_button(self) -> None:
        self.click(self.LOGIN_BUTTON)

    @allure.step("User logs in")
    def login_existing_user(self, phone_number: str, password: str, username: str) -> None:
        self.click_login_icon()
        self.fill_phone_number(phone_number)
        self.click_start_exploring()
        self.fill_password(password)
        self.click_login_button()
        assert self.get_user_name() == "Hi, "+username

    @allure.step("User clicks to change country code")
    def click_code_country(self) -> None:
        self.click(self.COUNTRY_CODE_COMBOBOX)

    @allure.step("Return country code")
    def get_code_country(self) -> str:
        return self.get_text(self.COUNTRY_CODE)

    @allure.step("Return image url")
    def get_country_name(self) -> str:
        return self.get_image_url(self.COUNTRY_FLAG)

   # TODO: Add login for new user with verification code
