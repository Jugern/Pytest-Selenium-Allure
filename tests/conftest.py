import allure
import random
import pytest

from dotenv import load_dotenv
from os import environ, getenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

# настройка окружения в зависимости от запуска
if 'url_selenium_grid' in environ:
    url_selenium_grid = environ.get('url_selenium_grid')
    port_selenium_grid = environ.get('port_selenium_grid')
    selector_selenium_grid = environ.get('selector')
elif 'port_selenium_grid' in environ:
    url_selenium_grid = 'selenium-hub'
    port_selenium_grid = environ.get('port_selenium_grid')
    selector_selenium_grid = '/wd/hub'
else:
    load_dotenv()
    url_selenium_grid = getenv('url_selenium_grid')
    port_selenium_grid = getenv('port_selenium_grid')
    selector_selenium_grid = getenv('selector')

@allure.epic("Start browser driver.")
@pytest.fixture(scope="function")
def browser() -> webdriver:
    """
    Fixture для инициализации драйвера браузера.
    Возвращает:
        WebDriver: Экземпляр драйвера браузера.
    Вызывает:
        NotImplementedError: Если указанный браузер не поддерживается.
    """
    remote_url = f"http://{url_selenium_grid}:{port_selenium_grid}{selector_selenium_grid}"

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

    local_browser_list = [local_firefox, local_chrome, local_edge, ]
    docker_browser_list = [docker_firefox, docker_chrome, docker_edge, ]
    browser = random.choice(docker_browser_list)()
    with allure.step(f"Запускается браузер {browser.name}"):
        ...
    yield browser
    with allure.step(f"Браузер {browser.name} закрывается"):
        ...
    browser.quit()
