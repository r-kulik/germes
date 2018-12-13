# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel
from main_ui import Ui_MainWindow
import json
import datetime
from helper import ourformateDate, parser, boolean, rememberAll, toDate
import time
import os
from PyQt5.QtWidgets import QInputDialog
import random


class Example(QMainWindow, Ui_MainWindow):
	
	def __init__(self):
		self.current_version = '0.2'
		super().__init__()
		self.setupUi(self)
		self.setWindowTitle("Гермес - Финансовый помощник")
		self.label_4.setText(self.current_version)
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
		init_tuple = rememberAll()
		self.balance = init_tuple[0]
		self.debt = init_tuple[1]
		self.listWidget.addItems(init_tuple[2])
		parser(self)
		self.pushButton_5.clicked.connect(self.clearCash)
		self.pushButton_4.clicked.connect(self.showSettings)
		self.pushButton_2.clicked.connect(self.showTransactionList)

	def showTransactionList(self):
		os.popen("transactionlist.py")

	def showSettings(self):
		os.popen("typesettingswindow.py")

	def add_transaction(self):
		with open("inoutcome.json") as inoutcome:
			a = inoutcome.read()
			inoutcome_dictionary = json.loads(a)
			# print(inoutcome_dictionary)
		current_time = str(time.time())
		written_dict = {}
		# print(inoutcome_dictionary)
		try:
			written_dict["name"] = self.lineEdit.text()
			written_dict["type"] = self.type_dict[self.combotext2]
			written_dict["operand"] = self.combotext
			written_dict["summ"] = float(self.lineEdit_2.text())
		except Exception:
			self.label_4.setText("Введите все или введите корректно")
		else:
			self.label_4.setText(self.current_version)
			if current_time in inoutcome_dictionary:
				current_time += 1
			inoutcome_dictionary[current_time] = written_dict
			# print(inoutcome_dictionary)
			# print(written_dict)
			# print(written_dict["type"])["summ"]
			if written_dict["type"] == "spend":
				self.balance -= written_dict["summ"]
			elif written_dict["type"]  == "reciept":
				self.balance += written_dict["summ"]
			elif written_dict["type"] == "loan":
				self.balance -= written_dict["summ"]
				self.debt += written_dict["summ"]
			elif written_dict["type"] == "borrow":
				# print('DONE')
				# print(self.balance, self.debt)
				# print(written_dict["summ"])
				self.balance = self.balance + written_dict["summ"]
				self.debt = self.debt - written_dict["summ"]
				# print(self.balance, self.debt)


			# print(inoutcome_dictionary)
			with open("inoutcome.json", 'w') as inoutcome:
				json.dump(inoutcome_dictionary, inoutcome)
		try:
			# print(self.balance, self.debt)
			parser(self)
			short_report = ' '.join([toDate(current_time),
								 	written_dict["name"],
								 	boolean(written_dict["type"]),
								 	str(written_dict["summ"])])
			self.listWidget.clear()
			self.listWidget.addItems(rememberAll()[2])
			self.label_4.setText(self.current_version)

		except KeyboardInterrupt:
			pass

	def combox2Active(self, text):
		self.combotext2 = text
		with open('transaction_types.json', 'r', encoding='utf-8') as transaction_types_file:
			transaction_types = json.loads(transaction_types_file.read())
		if text == 'Заработок':
			transaction_types_income = transaction_types["reciept"]
			self.comboBox.clear()
			self.comboBox.addItems(transaction_types_income)
			self.comboBox.activated[str].connect(self.comboxActive)
		elif text == 'Трата':
			transaction_types_outcome = transaction_types['spend']			
			self.comboBox.clear()
			self.comboBox.addItems(transaction_types_outcome)
			self.comboBox.activated[str].connect(self.comboxActive)

		elif text == 'Взятие в долг':
			self.comboBox.clear()
			self.comboBox.addItems(transaction_types["borrow"])
			self.comboBox.activated[str].connect(self.comboxActive)

		elif text == 'Предоставление долга':
			self.comboBox.clear()
			self.comboBox.addItems(transaction_types["loan"])
			self.comboBox.activated[str].connect(self.comboxActive)

	def comboxActive(self, text2):
		self.combotext = text2
		# print(self.combotext2, self.combotext)

	def clearCash(self):
		s1 = random.randint(1, 11)
		s2 = random.randint(1, 11)
		summ = s1 + s2
		i, okBtnPressed = QInputDialog.getInt(self,
											  "Вы действительно хотите удалить все?",
											  "Сколько будет " + str(s1) + '+' + str(s2),
											  0, 0, 100, 1)
		if okBtnPressed:
			if i == summ:
				with open("inoutcome.json", 'w') as inoutcome:
					inoutcome.write('{}')
				init_tuple = rememberAll()
				self.balance = init_tuple[0]
				self.debt = init_tuple[1]
				self.listWidget.clear()
				self.listWidget.addItems(init_tuple[2])
				parser(self)
			else:
				self.label_4.setText('Неправильно решен пример лол')


app = QApplication(sys.argv)
ex = Example()
ex.show()
sys.exit(app.exec_())