from .base_page import BasePage
from .locators import LoginPageLocators, MainPageLocators, DepositPageLocators, \
    WithDrawPageLocators, TransactionPageLocators

import time, csv, allure
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class MainPage(BasePage):
    """"""

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

    @allure.step('Пополняем баланс на сумму "Фибоначи"')
    def put_a_deposit(self):
        self.browser.find_element(*DepositPageLocators.DEPOSIT_BUTTON).click()
        self.browser.find_element(*DepositPageLocators.DEPOSIT_AMOUNT).send_keys(self.fib_sum)
        time.sleep(0.5)
        self.browser.find_element(*DepositPageLocators.DEPOSIT_CLICK).click()
        time.sleep(0.5)
        self.await_browser.until(EC.text_to_be_present_in_element(MainPageLocators.BALLANCE_BANK, str(self.fib_sum)))

    @allure.step("Проверяем, что сумма пополнилась")
    def balance_after_depositing(self):
        assert self.browser.find_element(*MainPageLocators.BALLANCE_BANK).text == str(self.fib_sum), \
            "Депозит не совпадает с заданным значением суммы Фибоначчи"
        assert self.browser.find_element(*DepositPageLocators.DEPOSIT_SUCCESS).text == "Deposit Successful", \
            "Нет надписи об успешном пополнение депозита"

    @allure.step('Убавляем баланс на сумму "Фибоначи"')
    def put_a_withdraw(self):
        self.await_browser.until(EC.visibility_of_element_located(WithDrawPageLocators.WITHDRAW_BUTTON)).click()
        self.await_browser.until(EC.visibility_of_element_located(WithDrawPageLocators.WITHDRAW_FORM))
        self.await_browser.until(EC.visibility_of_element_located(WithDrawPageLocators.WITHDRAW_AMOUNT))\
            .send_keys(self.fib_sum)
        time.sleep(0.5)
        self.await_browser.until(EC.visibility_of_element_located(WithDrawPageLocators.WITHDRAW_CLICK)).click()
        time.sleep(0.5)

    @allure.step("Проверяем, что сумма убавилась и равна 0")
    def balance_after_withdraw(self):
        assert self.browser.find_element(*MainPageLocators.BALLANCE_BANK).text == "0", \
            "Сумма на счету не равна нулю"
        assert self.browser.find_element(*WithDrawPageLocators.WITHDRAW_SUCCESS).text == "Transaction successful", \
            "Нет надписи об успешном снятии средств"

    @allure.step("Переходим на страницу транзакций")
    def go_to_transactions_page(self):
        self.browser.find_element(*TransactionPageLocators.TRANSACTIONS_BUTTON).click()
        self.table = self.browser.find_element(*TransactionPageLocators.TRANSACTIONS_TABLE)
        if not self.table.text:
            self.page_back_next(TransactionPageLocators.TRANSACTIONS_BACK_BUTTON,
                                TransactionPageLocators.TRANSACTIONS_BUTTON,
                                TransactionPageLocators.TRANSACTIONS_TABLE)
            self.table = self.browser.find_element(*TransactionPageLocators.TRANSACTIONS_TABLE)

    @allure.step("Проверяем, что транзакции преобразованы")
    def converting_transactions(self):
        spisok = self.check_table(TransactionPageLocators.TRANSACTIONS_TABLE)
        if not spisok:
            assert False, "Транзакции не записаны в таблицу"
        data_time_credit = datetime.strptime(spisok[0], "%B %d, %Y %I:%M:%S %p")
        amount_credit = spisok[1]
        trans_type_credit = spisok[2]
        data_time_debit = datetime.strptime(spisok[3], "%B %d, %Y %I:%M:%S %p")
        amount_debit = spisok[4]
        trans_type_debit = spisok[5]
        self.dict_csv = {
            'creadit': [data_time_credit, amount_credit, trans_type_credit],
            'debit': [data_time_debit, amount_debit, trans_type_debit]
        }

    @allure.step("Проверяем, что транзакции есть")
    def check_transactions(self):
        assert len(self.dict_csv) == 2, "Транзакции не совпадают"
        assert self.dict_csv['creadit'][1] == self.dict_csv['debit'][1], \
            "Транзакции не совпадают по сумме"
        assert self.dict_csv['creadit'][2] == "Credit", "Транзакция Credit не совершена"
        assert self.dict_csv['debit'][2] == "Debit", "Транзакция Debit не совершена"

    @allure.step("Сохраняем транзакцию в файл")
    def create_transaction_file(self):
        with open('transactions.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Дата-времяТранзакции', 'Сумма', 'ТипТранзакции'])
            for transaction_type, transaction_data in self.dict_csv.items():
                date_time = transaction_data[0].strftime("%d %B %Y %H:%M:%S")
                amount = transaction_data[1]
                transaction_type = transaction_data[2]
                writer.writerow([date_time, amount, transaction_type])

    @allure.step("Загружаем транзакцию из файла в отчет allure")
    def attach_transaction_file(self):
        csv_file_path = 'transactions.csv'
        allure.attach.file(csv_file_path, name="transactions.csv", attachment_type=allure.attachment_type.CSV)





