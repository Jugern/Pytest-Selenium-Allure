import allure
import pytest
from dotenv import load_dotenv
from os import environ
from pages.main_page import MainPage

load_dotenv()
number_test = int(environ.get("number_test"))  # количество тестов


@allure.epic('Отчет для allure')
@allure.feature('Отчетность по тестам')
@allure.testcase('https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login')
@allure.title(f'Тестирование № ')
@pytest.mark.parametrize("test_num", range(number_test))
def test_go_to_login_page(browser, test_num: int):
    with allure.step(f'Проверка теста №{test_num + 1}'):
        link = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login"
        with allure.step(f'Инициализируем Page Object, передаем драйвер и url адрес.'):
            page = MainPage(browser, link)   # Инициализируем Page Object, передаем драйвер и url адрес
        page.open()                      # Открываем страницу
        page.should_be_login_link()      # Проверяем, что ссылка логина есть
        page.go_to_login_page()          # Выполняем метод страницы — переходим на страницу логина
        page.select_choise_login()       # Выбираем логин
        page.go_to_panel()               # Переходим на страницу панели
        page.put_a_deposit()             # Пополняем баланс на сумму "Фибоначи"
        page.balance_after_depositing()  # Проверяем, что сумма пополнялась
        page.put_a_withdraw()            # Убавляем баланс на сумму "Фибоначи"
        page.balance_after_withdraw()    # Проверяем, что сумма убавилась и равна 0
        page.go_to_transactions_page()   # Переходим на страницу транзакций
        page.converting_transactions()   # Проверяем, что транзакции преобразованы
        page.check_transactions()        # Проверяем, что транзакции есть
        page.create_transaction_file()   # Сохраняем транзакцию в файл
        page.attach_transaction_file()   # Загружаем транзакцию из файла в отчет allure
        with allure.step(f'Тестирование завершено.'):
            pass


