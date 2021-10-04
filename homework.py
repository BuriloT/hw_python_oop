"""Калькулятор денег и калорий."""
import datetime as dt
from typing import Optional, Union

format = '%d.%m.%Y'


class Calculator:
    """Родительский класс
    хранит общие функции."""
    week_date = dt.datetime.today().date() - dt.timedelta(days=7)
    today_date = dt.date.today()

    def __init__(self, limit):
        """Конструктор класса Calculator."""
        self.limit = limit
        self.records = []

    def add_record(self, record) -> None:
        """Сохраняет новую запись."""
        self.records.append(record)

    def get_today_stats(self) -> Union[int, float]:
        """Считает потраченное за сегодня."""
        count: int = 0
        return sum(count + i.amount for i in self.records
                   if i.date == self.today_date)

    def get_week_stats(self) -> Union[int, float]:
        """Считает потраченное за неделю."""
        count: int = 0
        return sum(count + i.amount for i in self.records
                   if self.today_date >= i.date > self.week_date)

    def get_remained(self) -> Union[int, float]:
        """Возвращает остаток на сегодня."""
        self.remained = self.limit - self.get_today_stats()
        return self.remained


class CashCalculator(Calculator):
    """Класс для подсчёта денег."""
    RUB_RATE: float = 1.0
    USD_RATE: float = 60.0
    EURO_RATE: float = 70.0
    currency_dict = {'rub': ('руб', RUB_RATE),
                     'usd': ('USD', USD_RATE),
                     'eur': ('Euro', EURO_RATE)}

    def get_today_cash_remained(self, currency: str) -> str:
        """Определяет, сколько ещё денег можно потратить сегодня в
        рублях, долларах или евро."""
        if currency not in self.currency_dict:
            raise ValueError('Валюта не поддерживается')
        remained = self.get_remained()
        if not remained:
            return 'Денег нет, держись'
        value, rate = self.currency_dict[currency]
        money: Union[int, float] = abs(remained / rate)
        if remained > 0:
            return f'На сегодня осталось {money:.2f} {value}'
        else:
            return f'Денег нет, держись: твой долг - {money:.2f} {value}'


class CaloriesCalculator(Calculator):
    """Класс для подсчёта калорий."""
    def get_calories_remained(self) -> str:
        """Определяет, сколько ещё калорий можно/нужно получить сегодня."""
        if self.get_remained() > 0:
            return (f'Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более'
                    f' {self.get_remained()} кКал')
        else:
            return 'Хватит есть!'


class Record:
    """Класс для удобства создания записей."""
    def __init__(self, amount: Union[int, float], comment: str,
                 date: Optional[str] = None) -> None:
        """Конструктор класса Record."""
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, format).date()
