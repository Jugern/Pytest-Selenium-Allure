import allure
import pytest

from pages.config.settings import Config
from pages.main_page import AllureReport, DepositPage, MainPage, TransacPage, WithdrawPage

number_test = Config.create_number_test()


@allure.epic('Отчет для allure')
@allure.feature('Отчетность по тестам')
@allure.testcase('https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login')
@allure.title(f'Тестирование № ')
@pytest.mark.parametrize("test_num", range(number_test))
def test_go_to_login_page(browser, value_number, test_num: int):
    with allure.step(f'Проверка теста №{test_num + 1}'):
        link = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login"
        with allure.step(f'Инициализируем Page Object, передаем драйвер и url адрес.'):
            page = MainPage(browser, link)   # Инициализируем Page Object, передаем драйвер и url адрес
        page.open()                          # Открываем страницу
        page.should_be_login_link()          # Проверяем, что ссылка логина есть
        page.go_to_login_page()              # Выполняем метод страницы — переходим на страницу логина
        page.select_choise_login()           # Выбираем логин
        page.go_to_panel()                   # Переходим на страницу панели

        deposit_page = DepositPage(browser, link)      # Инициализируем DepositPage
        deposit_page.put_a_deposit(value_number)       # Пополняем баланс на сумму "Фибоначи"
        deposit_page.balance_after_depositing()        # Проверяем, что сумма пополнялась

        withdraw_page = WithdrawPage(browser, link)    # Инициализируем WithdrawPage
        withdraw_page.put_a_withdraw(value_number)     # Убавляем баланс на сумму "Фибоначи"
        withdraw_page.balance_after_withdraw()         # Проверяем, что сумма убавилась и равна 0

        transac_page = TransacPage(browser, link)      # Инициализируем TransactionPage
        transac_page.go_to_transactions_page()         # Переходим на страницу транзакций
        transac_page.converting_transactions()         # Проверяем, что транзакции преобразованы

        allure_report = AllureReport(browser, link)            # Инициализируем AllureReport
        allure_report.create_transaction_file('transactions')  # Сохраняем транзакцию в файл, передаем название файла
        allure_report.attach_transaction_file()                # Загружаем транзакцию из файла в отчет allure

        with allure.step(f'Тестирование завершено.'):
            allure_report.clear()  # Очищаем данные, после оформления отчета
