import datetime
import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from statitics_ui import Ui_Dialog

from_millis = datetime.datetime.fromtimestamp
TODAY = datetime.datetime.today().strftime('%d.%m.%Y')
YESTERDAY = datetime.datetime.today() - datetime.timedelta(days=1)
MONTH_AGO = datetime.datetime.today() - datetime.timedelta(days=31)

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
    from_date = compareable(date_from)
    to_date = compareable(date_to)
    period_summ = period_sample.copy()
    for transaction in data:
        if from_date <= compareable(datetime_human(from_millis(int(transaction)))) <= to_date:
            period_summ[data[transaction]["type"]]["summ"] += int(data[transaction]["summ"])
            period_summ[data[transaction]["type"]]["operands"].append(data[transaction]["operand"])
    return period_summ


def datetime_human(data):  # тупо из datetime в формат day.month.year
    return "{day}.{month}.{year}".format(**{
        "year": data.year,
        "month": data.month,
        "day": data.day,
    })


def compareable(datestr):
    return int("".join(["{0:>2}".format(i) for i in datestr.split(".")][::-1]))


def pie_diagram(counted_data, hand=False, show=False):  # круговая диаграмма расходов за период
    if hand:
        with plt.xkcd():
            pie_diagram(counted_data, show=show)
    else:
        labels = 'Мне Должны', 'Потратил', 'Я должен', 'Получил'
        sizes = [counted_data["loan"]["summ"], counted_data["spend"]["summ"], counted_data["borrow"]["summ"],
                 counted_data["reciept"]["summ"]]
        explode = (0.1, 0.1, 0.1, 0.1)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90)
        ax1.axis('equal')

    if show:
        plt.show()
        plt.rcdefaults()
        return None
    plt.savefig("pie_diagram.png")
    plt.rcdefaults()
    return "pie_diagram.png"


def horizontal_diagram(counted_data, hand=False, show=False):
    if hand:
        with plt.xkcd():
            horizontal_diagram(counted_data, show=show)
    else:
        labels = 'Мне должны', 'Потратил', 'Я должен', 'Получил'
        y_pos = np.arange(len(labels))
        fig, ax = plt.subplots()
        performance = np.asarray(
            [counted_data["loan"]["summ"], counted_data["spend"]["summ"], counted_data["borrow"]["summ"],
             counted_data["reciept"]["summ"]])
        ax.barh(y_pos, performance, align='center',
                color='green', ecolor='black')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        plt.yticks(rotation=60)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Сумма в рублях')
        ax.set_title('Сводка')

    if show:
        plt.show()
        plt.rcdefaults()
        return None
    plt.savefig("horizontal_diagram.png")
    plt.rcdefaults()
    return "horizontal_diagram.png"


class TypeSettingsWindow(QMainWindow, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Сводка за период")
        diagram_types = ["Круговая", "Горизонтальная"]
        self.comboBox.addItems(diagram_types)
        diagram_appearances = ["От руки", "Обычная"]
        self.comboBox_2.addItems(diagram_appearances)
        self.label.setText("С даты (\"День.Месяц.Год\")")
        self.label_2.setText("По дату")
        self.showBtn.clicked.connect(self.onClick)

    def alert_error(self, message="Неверный формат даты"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("FormatError")
        msg.setInformativeText(message)
        msg.setWindowTitle("FormatError")
        msg.exec_()

    def onClick(self):
        diagram_type = self.comboBox.currentText()
        diagram_appearance = self.comboBox_2.currentText()
        hand = diagram_appearance == "От руки"
        diagram_types_relate = {
            "Круговая": pie_diagram,
            "Горизонтальная": horizontal_diagram
        }

        date_from = self.lineEdit.text()
        date_to = self.lineEdit_2.text()
        try:
            if date_to == date_from == "":
                data = count_all()
            elif date_from.count(".") == 2 or date_to.count(".") == 2 or compareable(date_to) == compareable(date_from):
                if date_from != "":
                    compareable(date_from)
                    data = count_day(date_from)
                else:
                    compareable(date_to)
                    data = count_day(date_to)
            elif date_from.count(".") == 2 and date_to.count(".") == 2:
                if compareable(date_to) < compareable(date_from):
                    date_to, date_from = date_from, date_to
                data = count_period(date_from, date_to)
            else:
                raise ValueError
        except Exception as e:
            self.alert_error(e)
            return
        if data != {'spend': {'summ': 0, 'operands': []}, 'reciept': {'summ': 0, 'operands': []},
                    'borrow': {'summ': 0, 'operands': []}, 'loan': {'summ': 0, 'operands': []}}:
            diagram_types_relate[diagram_type](data, hand, True)
        else:
            self.alert_error("empty list")
            return


app = QApplication(sys.argv)
ex = TypeSettingsWindow()
ex.show()
sys.exit(app.exec_())
