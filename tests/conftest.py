from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import pytest
from pages.country_code_page import SportyCountryCodePage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from pages.login_page import SportyLoginPage
from pages.nav_bar_page import SportyNavBarPage
import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os




def pytest_addoption(parser):
    # parser.addoption("--debug", choices=["chrome", "firefox"], help="Launch browser for debugging")
    parser.addoption("--run_option", choices=[ "grid","standalone"], default="local", help="Specify Selenium Grid mode (local or remote)")

def pytest_generate_tests(metafunc):
    browsers = ["chrome", "firefox"]
    if "browser" in metafunc.fixturenames:
        metafunc.parametrize("browser", browsers)


@pytest.fixture(scope="function")
def setup(request: pytest.FixtureRequest,browser):
    global driver
    # debug = request.config.getoption("--debug")
    run_option = request.config.getoption("--run_option")
    if(run_option=="standalone"):
        if (browser in ("chrome")):
            chrome_options = webdriver.ChromeOptions()
            chrome_options.set_capability(
                "goog:loggingPrefs", {"browser": "ALL"}
            )

        match browser:
            case "chrome":
                driver = webdriver.Chrome(service=ChromeService(
                    ChromeDriverManager().install()), options=chrome_options)
            case "firefox":
                firefox_options = webdriver.FirefoxOptions()
                driver = webdriver.Firefox(service=FirefoxService(
                    GeckoDriverManager().install()), options=firefox_options)
    if(run_option=="grid"):
        ip = os.environ.get('HUB_HOST_NAME')
        if(not ip):
            raise  ValueError("You have not pass the ip value when running docker. Please run by pass env variable as follow docker run -e IP_ADDRESS=<GRID_IP_ADDRESS> <image_name>")
        SELENIUM_HUB = "http://{0}:4444".format(ip)
        print("----------------------------")
        print(SELENIUM_HUB)
        if (browser in ("chrome")):
            options = webdriver.ChromeOptions()
            driver = webdriver.Remote(command_executor=SELENIUM_HUB,options=options)
        if (browser in ("firefox")):
            options = webdriver.FirefoxOptions()
            driver = webdriver.Remote(command_executor=SELENIUM_HUB,options=options)
    

   
    try:      
        driver.get("https://sporty.com/news/latest")
        # make sure the page is loaded
        wait = WebDriverWait(driver, 60)
        wait.until(expected_conditions.visibility_of_element_located(
            ((By.XPATH, "//*[contains(text(),'Customise your')]"))))
        driver.implicitly_wait(10)
        request.cls.driver = driver
        request.cls.login_page = SportyLoginPage(driver)
        request.cls.nav_bar = SportyNavBarPage(driver)
        request.cls.country_code = SportyCountryCodePage(driver)


    
        yield driver
    except:
        allure.dynamic.tag(driver.capabilities["browserName"])
    finally:        
        allure.dynamic.tag(driver.capabilities["browserName"])
            
        allure.attach(driver.get_screenshot_as_png(),
                        name="Screenshot", attachment_type=AttachmentType.PNG)
        driver.quit()  



   


