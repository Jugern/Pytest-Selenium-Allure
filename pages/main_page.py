import os.path
import time

import allure
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

from .base_page import BasePage
from .locators import (LoginPageLocators,
                       MainPageLocators,
                       DepositLocators,
                       WithDrawLocators,
                       TransactionPageLocators,
                       )


class MainPage(BasePage):
    """
    Открывает главную страницу.
    Проверяет нахождение кнопки логина.
    Выбирает пользователя.
    Переходит на страницу главной панели.
    """

    @allure.step("Проверяем, что ссылка логина есть")
    def should_be_login_link(self):
        assert self.is_element_present(*LoginPageLocators.LOGIN_LINK), "Кнопки логина не найдены"

    @allure.step("Выполняем метод страницы — переходим на страницу логина")
    def go_to_login_page(self):
        login_link = self.browser.find_element(*LoginPageLocators.LOGIN_LINK)
        login_link.click()

    @allure.step("Выбираем логин")
    def select_choise_login(self):
        select = Select(self.browser.find_element(*LoginPageLocators.SELECT_USER))
        select.select_by_visible_text("Harry Potter")

    @allure.step("Переходим на страницу панели")
    def go_to_panel(self):
        self.browser.find_element(*LoginPageLocators.LOGIN_CLICK_BUTTON).click()


class DepositPage(BasePage):
    """
    Производит пополнение баланса на счет

    Methods:
        put_a_deposit(number): пополняет баланс на сумму number
        balance_after_depositing(): проверяет, что сумма пополнилась

    """
    @allure.step('Пополняем баланс на сумму "Фибоначи"')
    def put_a_deposit(self, number):
        self.await_browser.until(ec.visibility_of_element_located(DepositLocators.DEPOSIT_BUTTON)).click()
        self.await_browser.until(ec.visibility_of_element_located(DepositLocators.DEPOSIT_FORM))
        self.await_browser.until(ec.visibility_of_element_located(DepositLocators.DEPOSIT_AMOUNT)).send_keys(number)
        time.sleep(0.5)
        self.browser.find_element(*DepositLocators.DEPOSIT_CLICK).click()
        self.utility.deposit(number)
        time.sleep(0.5)

    @allure.step("Проверяем, что сумма пополнилась")
    def balance_after_depositing(self):
        assert self.browser.find_element(*MainPageLocators.BALANCE_BANK).text == str(self.utility.start_number), \
            "После внесения депозита сумма не совпадает с итоговой суммой."
        assert self.browser.find_element(*DepositLocators.DEPOSIT_SUCCESS).text == "Deposit Successful", \
            "Нет надписи об успешном пополнение депозита"


class WithdrawPage(BasePage):
    """
    Производит вывода средств со счета

    Methods:
        put_a_withdraw(number): выводит средства со счета на сумму number
        balance_after_withdraw(): проверяет, что сумма убавилась на number и равна self.utility.start_number

    """

    @allure.step('Убавляем баланс на сумму "Фибоначи"')
    def put_a_withdraw(self, number):
        self.await_browser.until(ec.visibility_of_element_located(WithDrawLocators.WITHDRAW_BUTTON)).click()
        self.await_browser.until(ec.visibility_of_element_located(WithDrawLocators.WITHDRAW_FORM))
        self.await_browser.until(ec.visibility_of_element_located(WithDrawLocators.WITHDRAW_AMOUNT))\
            .send_keys(number)
        time.sleep(0.5)
        self.await_browser.until(ec.visibility_of_element_located(WithDrawLocators.WITHDRAW_CLICK)).click()
        self.utility.withdraw(number)
        time.sleep(0.5)

    @allure.step("Проверяем, что сумма убавилась и равна 0")
    def balance_after_withdraw(self):
        assert self.browser.find_element(*MainPageLocators.BALANCE_BANK).text == str(self.utility.start_number), \
            "Сумма после вывода не совпадает с итоговой суммой."
        assert self.browser.find_element(*WithDrawLocators.WITHDRAW_SUCCESS).text == "Transaction successful", \
            "Нет надписи об успешном снятии средств"


class TransacPage(BasePage):
    """
    Производит переход на страницу транзакций и преобразовывает транзакции в таблицу.

    Methods:
        go_to_transactions_page(): переходим на страницу транзакций
        converting_transactions(): преобразовывает транзакции в таблицу
        check_transactions(): проверяет, что транзакции преобразованы в таблицу

    """

    @allure.step("Переходим на страницу транзакций")
    def go_to_transactions_page(self):
        assert self.browser.find_element(*MainPageLocators.BALANCE_BANK).text == str(self.utility.start_number), \
            "Сумма после всех транзакций не совпадает с итоговой суммой."
        self.browser.find_element(*TransactionPageLocators.TRANSACTIONS_BUTTON).click()
        self.utility.table = self.browser.find_element(*TransactionPageLocators.TRANSACTIONS_TABLE)
        if not self.utility.table.text:
            self.page_back_next(TransactionPageLocators.TRANSACTIONS_BACK_BUTTON,
                                TransactionPageLocators.TRANSACTIONS_BUTTON,
                                TransactionPageLocators.TRANSACTIONS_TABLE)
            self.utility.table = self.browser.find_element(*TransactionPageLocators.TRANSACTIONS_TABLE)

    @allure.step("Проверяем, что транзакции преобразованы")
    def converting_transactions(self):
        trans_table = self.converting_table()
        assert trans_table, "Транзакции не записаны в таблицу"
        assert len(trans_table) == self.utility.get_all_actions(), "Количество транзакции не совпадает"
        self.utility.create_table(trans_table)


class AllureReport(BasePage):
    """
    Сохраняем транзакции в файл и передаем его в отчет allure

    Methods:
        create_transaction_file(file_name): сохраняем транзакцию в файл
        attach_transaction_file(): прикрепляем файл в отчет allure
        clear_data(): очищаем все данные после создания отчета

    """

    @allure.step("Сохраняем транзакцию в файл")
    def create_transaction_file(self, file_name):
        file_name = self.utility.create_csv_file(file_name)
        assert os.path.isfile(file_name), "CSV файла не создался"

    @allure.step("Загружаем транзакцию из файла в отчет allure")
    def attach_transaction_file(self):
        csv_file_path = self.utility.get_filename()
        allure.attach.file(csv_file_path, name="transactions.csv", attachment_type=allure.attachment_type.CSV)

    def clear(self):
        """ Очищение данных """
        self.clear_data()
