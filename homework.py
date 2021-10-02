import datetime as dt

format = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        count = 0
        for i in self.records:
            if i.date == dt.datetime.today().date():
                count += i.amount
        return count

    def get_week_stats(self):
        count = 0
        today_date = dt.datetime.today().date()
        week_date = dt.datetime.today().date() - dt.timedelta(days=7)
        for i in self.records:
            if today_date >= i.date > week_date:
                count += i.amount
        return count


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    USD_RATE = 60.0
    EURO_RATE = 70.0
    currency_dict = {'rub': ('руб', RUB_RATE),
                     'usd': ('USD', USD_RATE),
                     'eur': ('Euro', EURO_RATE)}

    def get_today_cash_remained(self, currency):
        value, rate = self.currency_dict[currency]
        cash = self.limit - self.get_today_stats()
        money = abs(cash / rate)
        if cash > 0:
            return f'На сегодня осталось {money:.2f} {value}'
        elif cash == 0:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {money:.2f} {value}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories = self.limit - self.get_today_stats()
        if 0 < calories:
            return (f'Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более'
                    f' {calories} кКал')
        else:
            return 'Хватит есть!'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.today().date()
        else:
            self.date = dt.datetime.strptime(date, format).date()
