import allure
import datetime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Any, Union


class BasePage:

    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)
        self.await_browser = WebDriverWait(self.browser, timeout)
        self.fib_sum = self.chislo_fibonaci()
        self.table = None  # данные по всей таблице
        self.dict_csv = dict()  # словарь для сохранения в формате csv

    def chislo_fibonaci(self) -> int:
        fib1 = fib2 = 1
        n = datetime.datetime.now().day - 1
        while n > 0:
            fib1, fib2 = fib2, fib1 + fib2
            n -= 1
        return fib2

    @allure.step('Открываем страницу')
    def open(self) -> None:
        self.browser.get(self.url)

    def is_element_present(self, how, what) -> bool:
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def await_element_present(self, how, what) -> None:
        # Метод для проверки наличия элемента на странице через значения параметров
        self.browser.until(EC.visibility_of_element_located((how, what)))

    def check_selector(self, selector: tuple) -> None:
        # Метод для проверки наличия элемента на странице через кортеж
        self.await_browser.until(EC.visibility_of_element_located(selector))

    def page_back_next(self, selector_back: tuple, selector_next: tuple, table: tuple) -> None:
        # Метод для проверки наличия данных в таблице, если нет,
        # то переходим на предыдущую страницу с возвратом на страницу.
        i = 18
        while i:
            if not self.table.text:
                self.await_browser.until(EC.element_to_be_clickable(selector_back)).click()
                self.await_browser.until(EC.element_to_be_clickable(selector_next)).click()
                self.table = self.await_browser.until(EC.visibility_of_element_located(table))
                i -= 1
            else:
                i = 0

    def converting_table(self) -> list(Any):
        # Метод для конвертации таблицы в список значений
        # Ожидаем:
        #   1 значение: дата, 2 значение: сумма, 3 значение: Дебит или Кредит
        #   4 значение: дата, 5 значение: сумма, 6 значение: Дебит или Кредит
        table = self.table
        convert = list()
        for i in table.find_elements(By.TAG_NAME, "td"):
            convert.append(i.text)
        return convert

    def check_table(self, transactions_table: tuple) -> list[Union[str, int]]:
        # Метод преобразования список значений в словарь для сохранения в формате csv
        i = 5
        spisok = self.converting_table()
        while i:
            if len(spisok) != 6:
                self.table = self.await_browser.until(EC.visibility_of_element_located(
                    transactions_table))
                spisok = self.converting_table()
                i -= 1
            else:
                return spisok
        return list()




