import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .utility import Utility


class BasePage:
    """
    Класс для работы со страницей

    Attributes:
        browser (selenium.webdriver): Драйвер браузера
        url (str): URL адрес для открываемой страницы
        await_browser (webdriver.support.ui.WebDriverWait): Ожидание элемента (10 секунд)
        utility (Utility): инициализация singleton где хранятся методы и атрибуты для работы с данными

    """

    def __init__(self, browser, url, timeout=10):
        super().__init__()
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)
        self.await_browser = WebDriverWait(self.browser, timeout)
        self.utility = Utility()

    @allure.step('Открываем страницу')
    def open(self) -> None:
        """ Открывает страницу url"""
        self.browser.get(self.url)

    def is_element_present(self, how, what) -> bool:
        """ Проверяет наличие элемента на странице

        Args:
            how (webdriver.support.ui.By): Определение элемента (xpath, css, id, name)
            what (str): Имя элемента для поиска

        Returns:
            bool: Проверка наличия элемента True или False

        """
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def check_selector(self, selector: tuple) -> None:
        """ Метод для проверки наличия элемента на странице через кортеж

        Args:
            selector (tuple): Определение элемента (xpath, css, id, name) и имя элемента

        """
        self.await_browser.until(ec.visibility_of_element_located(selector))

    def page_back_next(self, selector_back: tuple, selector_next: tuple, table: tuple) -> None:
        """Метод для проверки наличия данных в таблице, если нет,
        то переходим на предыдущую страницу с возвратом на страницу.

        Args:
            selector_back (tuple): Определение элемента (xpath, css, id, name) и имя элемента для перехода назад
            selector_next (tuple): Определение элемента (xpath, css, id, name) и имя элемента для перехода вперед
            table (tuple): Определение элемента (xpath, css, id, name) и имя элемента для таблицы

        """
        i = 18
        while i:
            if not self.utility.table.text:
                self.await_browser.until(ec.element_to_be_clickable(selector_back)).click()
                self.await_browser.until(ec.element_to_be_clickable(selector_next)).click()
                self.utility.table = self.await_browser.until(ec.visibility_of_element_located(table))
                i -= 1
            else:
                i = 0

    def converting_table(self) -> list:
        """ Метод конвертирует таблицу в список

        Returns:
            list: Возвращает список из таблицы транзакций в виде [[первая транзакция], [вторая транзакция], и т.д.]

        """
        table = self.utility.table
        convert = list()
        for j in table.find_elements(By.TAG_NAME, "tr"):
            value_row = list()
            for i in j.find_elements(By.TAG_NAME, "td"):
                value_row.append(i.text)
            convert.append(value_row)
        return convert

    def clear_data(self) -> None:
        """ Метод для очистки данных в Singleton"""
        Utility.delete_instance()
