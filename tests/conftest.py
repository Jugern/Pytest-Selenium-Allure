import random

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from pages.config.settings import Config


@allure.epic("Start browser driver.")
@pytest.fixture(scope="function")
def browser() -> webdriver:
    """
    Fixture для инициализации драйвера браузера.
    Если указать в переменной browser при random.choice() передать local_browser_list, то будет локальный запуск.

    Returns:
        WebDriver: Экземпляр драйвера браузера.
    """

    remote_url = Config.create_remote_url()

    @allure.description("Start local Firefox browser driver.")
    def local_firefox() -> webdriver:
        """
        Инициализация локального драйвера браузера Firefox.
        Возвращает:
            WebDriver: Экземпляр драйвера браузера Firefox.
        """
        binary = './FirefoxPortable/App/Firefox64/Firefox.exe'
        driver = './FirefoxPortable/geckodriver-v0.33.0-win64/geckodriver.exe'
        service = Service(executable_path=driver)
        options = webdriver.FirefoxOptions()
        options.binary_location = binary
        driver = webdriver.Firefox(service=service, options=options)
        return driver

    @allure.description("Start local Chrome browser driver.")
    def local_chrome() -> webdriver:
        """
        Инициализация локального драйвера браузера Chrome.
        Возвращает:
            WebDriver: Экземпляр драйвера браузера Chrome.
        """
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        return driver

    @allure.description("Start local Edge browser driver.")
    def local_edge() -> webdriver:
        """
        Инициализация локального драйвера браузера Edge.
        Возвращает:
            WebDriver: Экземпляр драйвера браузера Edge.
        """
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(options=options)
        return driver

    @allure.description("Start docker Firefox browser driver.")
    def docker_firefox() -> webdriver:
        """
        Инициализация драйвера браузера Firefox для Docker или просто в url selenium grid.
        Возвращает:
            WebDriver: Экземпляр драйвера браузера Firefox.
        """
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        driver = webdriver.Remote(command_executor=remote_url, options=options)
        return driver

    @allure.description("Start docker Chrome browser driver.")
    def docker_chrome() -> webdriver:
        """
        Инициализация драйвера браузера Chrome для Docker или просто в url selenium grid.
        Возвращает:
            WebDriver: Экземпляр драйвера браузера Chrome.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Remote(command_executor=remote_url, options=options)
        return driver

    @allure.description("Start docker Edge browser driver.")
    def docker_edge() -> webdriver:
        """
        Инициализация драйвера браузера Edge для Docker или просто в url selenium grid.
        Возвращает:
            WebDriver: Экземпляр драйвера браузера Edge.
        """
        options = webdriver.EdgeOptions()
        driver = webdriver.Remote(command_executor=remote_url, options=options)
        return driver

    # local_browser_list = [local_firefox, local_chrome, local_edge, ]
    docker_browser_list = [docker_firefox, docker_chrome, docker_edge, ]
    browser = random.choice(docker_browser_list)()
    with allure.step(f"Запускается браузер {browser.name}"):
        ...
    yield browser
    with allure.step(f"Браузер {browser.name} закрывается"):
        ...
    browser.quit()


@pytest.fixture
def value_number():
    """
    Значение, которое будет передаваться в тестовый метод
    """
    number = Config.sum_number_fibonacci()
    return number
