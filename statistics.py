import datetime
import json

from_millis = datetime.datetime.fromtimestamp
TODAY = datetime.datetime.today().strftime('%d-%m-%Y')
TOMORROW = datetime.datetime.today() - datetime.timedelta(days=1)
MONTH_AGO = datetime.datetime.today() - datetime.timedelta(month=1)

period_sample = {
    "spend": {  # просто траты
        "summ": 0,
        "operands": []
    },
    "reciept": {  # просто поднял
        "summ": 0,
        "operands": []
    },
    "borrow": {  # ты Саня и ты занял бабосов
        "summ": 0,
        "operands": []
    },
    "loan": {  # у тя Саня занял ловешку
        "summ": 0,
        "operands": []
    }
}


def get_transactions():  # достать все транзакции
    with open("inoutcome.json", "rb") as file:
        data = json.load(file)
    return data


def count_day(string_day=TODAY):  # сводка за день string_day [22.12.2018]
    data = get_transactions()
    day_summ = period_sample.copy()
    for i in data:
        if datetime_human(from_millis(int(i))) == string_day:
            day_summ[data[i]["type"]]["summ"] += int(data[i]["summ"])
            day_summ[data[i]["type"]]["operands"].append(data[i]["operand"])
    return day_summ


def count_all():
    data = get_transactions()
    all_summ = period_sample.copy()
    for i in data:
        all_summ[data[i]["type"]]["summ"] += int(data[i]["summ"])
        all_summ[data[i]["type"]]["operands"].append(data[i]["operand"])
    return all_summ


def count_period(date_from, date_to):
    data = get_transactions()
    from_date = int("".join(["{0:>2}".format(i) for i in date_from.split(".")][::-1]))
    to_date = int("".join(["{0:>2}".format(i) for i in date_to.split(".")][::-1]))
    period_summ = period_sample.copy()
    for transaction in data:
        if from_date <= int("".join(
                ["{0:>2}".format(i) for i in datetime_human(from_millis(int(transaction))).split(".")][
                ::-1])) <= to_date:
            period_summ[data[transaction]["type"]]["summ"] += int(data[transaction]["summ"])
            period_summ[data[transaction]["type"]]["operands"].append(data[transaction]["operand"])
    return period_summ


def datetime_human(data):  # тупо из datetime в формат day.month.year
    return "{day}.{month}.{year}".format(**{
        "year": data.year,
        "month": data.month,
        "day": data.day,
    })
