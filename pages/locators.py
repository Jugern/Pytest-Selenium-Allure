from typing import Tuple

from selenium.webdriver.common.by import By


class LoginPageLocators:
    """
    Здесь хранятся локаторы для страницы логина
    """
    LOGIN_LINK = (By.CSS_SELECTOR,
                  "body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button")
    SELECT_USER = (By.CSS_SELECTOR, "#userSelect")
    LOGIN_CLICK_BUTTON = (By.CSS_SELECTOR, "body > div > div > div.ng-scope > div > form > button")


class MainPageLocators:
    """
    Здесь хранятся локаторы для главной панели
    """
    BALLANCE_BANK = (By.CSS_SELECTOR, "body > div > div > div.ng-scope > div > div:nth-child(3) > strong:nth-child(2)")
    TRANSACTIONS_BUTTON = (By.CSS_SELECTOR,
                           "body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(1)")


class DepositPageLocators:
    """
    Здесь хранятся локаторы для взаимодействия с пополнением стредств
    """
    DEPOSIT_BUTTON = (By.CSS_SELECTOR,
                      "body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(2)")
    DEPOSIT_FORM = (By.CSS_SELECTOR,
                    'form[ng-submit="deposit()"]')
    DEPOSIT_AMOUNT = (By.CSS_SELECTOR,
                      "div > div.container-fluid.mainBox.ng-scope > div > form > div > input")
    DEPOSIT_CLICK = (By.CSS_SELECTOR,
                     "div > div.container-fluid.mainBox.ng-scope > div > form > button")
    DEPOSIT_SUCCESS = (By.CSS_SELECTOR,
                       "div > div.container-fluid.mainBox.ng-scope > div > span")


class WithDrawPageLocators:
    """
    Здесь хранятся локаторы для взаимодействия с выводом стредств
    """
    WITHDRAW_BUTTON = (By.CSS_SELECTOR,
                       "body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(3)")
    WITHDRAW_FORM = (By.CSS_SELECTOR,
                    'form[ng-submit="withdrawl()"]')
    WITHDRAW_AMOUNT = (By.CSS_SELECTOR,
                       'div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > div > input')
    WITHDRAW_CLICK = (By.CSS_SELECTOR,
                      "div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button")
    WITHDRAW_SUCCESS = (By.CSS_SELECTOR,
                        "div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > span")


class TransactionPageLocators:
    """
    Здесь хранятся локаторы для взаимодействия с таблицей транзакций
    """
    TRANSACTIONS_BUTTON = (By.CSS_SELECTOR,
                           "body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(1)")
    TRANSACTIONS_TABLE = (By.CSS_SELECTOR,
                          "body > div > div > div.ng-scope > div > div:nth-child(2) > table > tbody")
    TRANSACTIONS_BACK_BUTTON = (By.CSS_SELECTOR,
                                "body > div > div > div.ng-scope > div > div.fixedTopBox > button:nth-child(1)")
