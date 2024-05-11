from selenium.webdriver.common.by import By


class LoginPageLocators:
    """
    Здесь хранятся локаторы для страницы логина
    """
    LOGIN_LINK = (By.XPATH, '//button[text()="Customer Login"]')
    SELECT_USER = (By.CSS_SELECTOR, "#userSelect")
    LOGIN_CLICK_BUTTON = (By.XPATH, '//button[text()="Login"]')


class MainPageLocators:
    """
    Здесь хранятся локаторы для главной панели
    """
    BALANCE_BANK = (By.XPATH, "//div[@class='center']/strong[2]")


class DepositLocators:
    """
    Здесь хранятся локаторы для взаимодействия с пополнением средств
    """
    DEPOSIT_BUTTON = (By.XPATH, '//button[@ng-click="deposit()"]')
    DEPOSIT_FORM = (By.CSS_SELECTOR, 'form[ng-submit="deposit()"]')
    DEPOSIT_AMOUNT = (By.XPATH, '//form[@name="myForm"]//input[@placeholder="amount"]')
    DEPOSIT_CLICK = (By.XPATH, '//form[@name="myForm"]/button[text()="Deposit"]')
    DEPOSIT_SUCCESS = (By.XPATH, '//div[@class="ng-scope"]/span[@ng-show="message"]')


class WithDrawLocators:
    """
    Здесь хранятся локаторы для взаимодействия с выводом средств
    """
    WITHDRAW_BUTTON = (By.XPATH, '//button[@ng-click="withdrawl()"]')
    WITHDRAW_FORM = (By.CSS_SELECTOR, 'form[ng-submit="withdrawl()"]')
    WITHDRAW_AMOUNT = (By.XPATH, '//form[@name="myForm"]//input[@placeholder="amount"]')
    WITHDRAW_CLICK = (By.XPATH, '//form[@name="myForm"]//button[text()="Withdraw"]')
    WITHDRAW_SUCCESS = (By.XPATH, '//div[@class="ng-scope"]/span[@ng-show="message"]')


class TransactionPageLocators:
    """
    Здесь хранятся локаторы для взаимодействия с таблицей транзакций
    """
    TRANSACTIONS_BUTTON = (By.XPATH, '//button[@ng-class="btnClass1"]')
    TRANSACTIONS_TABLE = (By.XPATH, '//table[@class="table table-bordered table-striped"]/tbody')
    TRANSACTIONS_BACK_BUTTON = (By.XPATH, '//button[@ng-click="back()"]')
