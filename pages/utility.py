import csv
from datetime import datetime


def singleton(cls):
    """ Декоратор singleton для класса Utility"""
    instances = {}

    def get_instance(*args, **kwargs):
        """ Возвращает экземпляр класса """
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    def delete_instance():
        """ Удаляет экземпляр класса """
        if cls in instances:
            del instances[cls]
    get_instance.delete_instance = delete_instance

    return get_instance


@singleton
class Utility:
    """
    Класс для работы с данными, нужно для общего доступа к изменениям в переменных.
    Является Singleton.

    Attributes:
        all_actions (dict): в словарь записываются количество выполненных операций с балансом
        start_number (int): начальная сумма равная 0, изменяется после выполнения операций с балансом

        dict_csv (dict): словарь для сохранения в формате csv
        _filename (str): имя csv файла для сохранения
        table (list): сохраненные данные транзакций по всей таблице

    """
    def __init__(self):
        self.all_actions = {
            'deposit': 0,
            'withdraw': 0
        }
        self.dict_csv = dict()
        self._filename = ''     # имя csv файла для сохранения
        self.start_number = 0   # начальная сумма
        self.table = None       # сохраненные данные транзакций по всей таблице

    def create_csv_file(self, filename: str):
        """Сохранение данных в csv файл

        Args:
            filename (str): имя csv файла

        Returns:
            _filename (str): имя csv файла, конечное название будет filename.csv

        """
        with open(f'{filename}.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Дата-времяТранзакции', 'Сумма', 'ТипТранзакции'])
            for transaction, transaction_data in self.dict_csv.items():
                for value in transaction_data:
                    date_time = value[0].strftime("%d %B %Y %H:%M:%S")
                    amount = value[1]
                    transaction_type = value[2]
                    writer.writerow([date_time, amount, transaction_type])
        self._filename = f'{filename}.csv'
        return self._filename

    def create_table(self, trans_table: list):
        """Сохранение данных в список

        Args:
            trans_table (list): список транзакций

        """
        for trans in trans_table:
            data_time = datetime.strptime(trans[0], "%B %d, %Y %I:%M:%S %p")
            amount = trans[1]
            trans_type = trans[2]
            self.dict_csv.setdefault(data_time, []).append([data_time, amount, trans_type])

    def get_all_actions(self) -> int:
        """Возвращает количество выполненных операций с балансом - withdraw, deposit"""
        return sum(self.all_actions.values())

    def get_filename(self):
        """Возвращает имя csv файла"""
        return self._filename

    def deposit(self, amount: int):
        """Увеличивает количество выполненных операций deposit и увеличивает start_number на amount"""
        self.all_actions['deposit'] += 1
        self.start_number += amount

    def withdraw(self, amount: int):
        """Увеличивает количество выполненных операций withdraw и уменьшает start_number на amount"""
        self.all_actions['withdraw'] += 1
        self.start_number -= amount  # TODO проверка на отрицательное число, если отрицательное - не уменьшать
