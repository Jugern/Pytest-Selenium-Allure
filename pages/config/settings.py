from datetime import datetime
from dotenv import load_dotenv
from os import environ, getenv


class Config:
    """
    Класс для создания конфигурации приложения.

    Данные из .env файла или all.env файла.
    В случае локального запуска используются значения из .env файла при помощи модуля dotenv.

    """

    @staticmethod
    def create_number_test() -> int:
        """Выбор числа тестов в зависимости от запуска или загруженного файла

        Returns:
            int: число тестов

        """
        try:
            if 'number_test' in environ:
                number_test = int(environ.get('number_test'))
            else:
                load_dotenv()
                number_test = int(getenv('number_test'))
        except ValueError:
            print('Неверный формат переменной number_test. Передано 1')
            return 1
        else:
            return number_test

    @staticmethod
    def create_remote_url():
        """Создание url адреса для selenium grid в зависимости от запуска или загруженного файла

        Returns:
            str: url адрес

        """
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
        return f"http://{url_selenium_grid}:{port_selenium_grid}{selector_selenium_grid}"

    @staticmethod
    def sum_number_fibonacci() -> int:
        """ Метод для вычисления суммы чисел Фибоначчи в зависимости от даты запуска

        Returns:
            fib2 (int): Сумма чисел Фибоначчи.

        """
        fib1 = fib2 = 1
        n = datetime.now().day - 1
        while n > 0:
            fib1, fib2 = fib2, fib1 + fib2
            n -= 1
        return fib2
