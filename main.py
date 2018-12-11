# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel
from main_ui import Ui_MainWindow
import json
import datetime
from helper import ourformateDate, parser
import time



class Example(QMainWindow, Ui_MainWindow):
	
	def __init__(self):
		current_version = '0.1'
		super().__init__()
		self.setupUi(self)
		self.setWindowTitle("Гермес - Финансовый помощник")
		self.label_4.setText(current_version)
		self.pushButton.clicked.connect(self.add_transaction)
		transaction_types = ['Заработок',
							 'Трата',
							 'Взятие в долг',
							 'Предоставление долга']
		self.comboBox_2.addItems(transaction_types)
		self.comboBox_2.activated[str].connect(self.combox2Active)
		self.type_dict = {"Заработок": "reciept",
						  "Трата": "spend",
						  "Взятие в долг": "borrow",
						  "Предоставление долга": "loan"}
		self.balance = 0
		self.debt = 0
		"""
		Здесь реализовать функцию вычисления баланса и всего прочего из кэша
		"""


	def add_transaction(self):
		with open("inoutcome.json") as inoutcome:
			a = inoutcome.read()
			inoutcome_dictionary = json.loads(a)
			# print(inoutcome_dictionary)
		current_date = ourformateDate(str(datetime.datetime.now()))
		written_dict = {}
		print(inoutcome_dictionary)
		try:
			written_dict["name"] = self.lineEdit.text()
			written_dict["type"] = self.type_dict[self.combotext2]
			written_dict["operand"] = self.combotext
			written_dict["summ"] = float(self.lineEdit_2.text())
			written_dict["time"] = int(round(time.time() * 1000))
		except Exception:
			self.label_4.setText("Введите все или введите корректно")
		else:
			if current_date in inoutcome_dictionary:
				inoutcome_dictionary[current_date].append(written_dict)
			else:
				inoutcome_dictionary[current_date] = [written_dict]
			# print(inoutcome_dictionary)
			print(written_dict)
			if written_dict["type"] == "spend":
				self.balance -= written_dict["summ"]
			elif written_dict["type"]  == "reciept":
				self.balance += written_dict["summ"]
			elif written_dict["type"] == "loan":
				self.balance -= written_dict["summ"]
				self.debt += written_dict["summ"]
			elif written_dict["type"] == "borrow":
				self.balance += written_dict["summ"]
				self.balance -= written_dict["summ"]


			# print(inoutcome_dictionary)
			with open("inoutcome.json", 'w') as inoutcome:
				json.dump(inoutcome_dictionary, inoutcome)
		parser(self)

	def combox2Active(self, text):
		self.combotext2 = text
		if text == 'Заработок':
			transaction_types_income = ['Зарплата',
										'Стипендия',
										'Пособие',
										'Аренда',
										'Другие типы дохода']
			self.comboBox.clear()
			self.comboBox.addItems(transaction_types_income)
			self.comboBox.activated[str].connect(self.comboxActive)
		elif text == 'Трата':
			transaction_types_outcome = ['Еда',
										 'Транспорт',
										 'Развлечения',
										 'ЖКХ и подобное',
										 'Образование и курсы',
										 'Ежемесячные траты',
										 'Обновления и одежда']
			self.comboBox.clear()
			self.comboBox.addItems(transaction_types_outcome)
			self.comboBox.activated[str].connect(self.comboxActive)

		else:
			self.comboBox.clear()
			self.comboBox.addItem(text)
			self.combotext = text

	def comboxActive(self, text2):
		self.combotext = text2
		print(self.combotext2, self.combotext)

app = QApplication(sys.argv)
ex = Example()
ex.show()
sys.exit(app.exec_())
