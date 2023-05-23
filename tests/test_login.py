from testData.login_page_data import LoginPageData
from tests.test_base import BaseTest
from selenium.webdriver.common.by import By
import allure
import pytest


@allure.story('Login functionality')
class TestLogin(BaseTest):
    @allure.description("User is not allowed to enter invalid phone number")
    @allure.title('User is not allowed to enter invalid phone number')
    def test_invalid_phone_number(self):
        self.nav_bar.click_login_icon()
        self.login_page.fill_phone_number("11111111111")
        self.login_page.click_start_exploring()
        error_message = self.driver.find_element(
            By.XPATH, "//*[contains(text(),'Incorrect username or password')]")
        assert error_message.is_displayed

    @allure.description("User is not allowed to enter alpha characters")
    @allure.title("User is not allowed to enter alpha characters")
    def test_invalid_input_number(self):
        self.nav_bar.click_login_icon()
        self.login_page.fill_phone_number("aaaa")
        assert (self.driver.find_element(
            *self.login_page.MOBILE_NUMBER).get_attribute("value")) == ""
        assert (self.driver.find_element(
            *self.login_page.START_EXPLORING).get_attribute("disabled"))
    # This is using an already created user
    # I would assume for sporty there is a way to create new users

    @allure.description("User is able to login")
    @allure.title("User is able to login,this should fail")
    def test_user_login(self):
        self.login_page.login_existing_user(
            "01116888790", "test", "alyaothman")

    @allure.description("User is able to change country code")
    @allure.title("User is able to change country code")
    def test_country_code_change(self, country_code_data):
        self.nav_bar.click_login_icon()
        self.login_page.click_code_country()
        self.country_code.click_country_code(country_code_data["country"])
        # This line to test console logs are captured
        self.driver.execute_script(
            'return console.log("Hello from the console log")')
        assert self.login_page.get_code_country() == country_code_data["code"]

    @pytest.fixture(params=LoginPageData.test_login_page_country_data)
    def country_code_data(self, request):
        return request.param
