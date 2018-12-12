# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from typesettingswindow_ui import Ui_MainWindow as SettingsUi_MainWindow
from PyQt5.QtWidgets import QInputDialog
import json
import os

class TypeSettingsWindow(QMainWindow, SettingsUi_MainWindow):
	
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setWindowTitle("Настройка категорий транзакций")
		self.pushButton.clicked.connect(self.showReciepts)
		self.pushButton_2.clicked.connect(self.showSpends)
		self.pushButton_3.clicked.connect(self.showBorrows)
		self.pushButton_4.clicked.connect(self.showLoans)
		with open("transaction_types.json", 'r', encoding='utf-8') as transaction_types_file:
			transaction_types = json.loads(transaction_types_file.read())
		self.transaction_types = transaction_types
		self.pushButton_6.clicked.connect(self.deleteType)
		self.currentgroup = ''
		self.pushButton_5.clicked.connect(self.addType)

	def showReciepts(self):
		self.listWidget.clear()
		self.listWidget.addItems(self.transaction_types["reciept"])
		self.currentgroup = 'reciept'

	def showSpends(self):
		self.listWidget.clear()
		self.listWidget.addItems(self.transaction_types["spend"])
		self.currentgroup = 'spend'

	def showBorrows(self):
		self.listWidget.clear()
		self.listWidget.addItems(self.transaction_types["borrow"])
		self.currentgroup = 'borrow'

	def showLoans(self):
		self.listWidget.clear()
		self.listWidget.addItems(self.transaction_types["loan"])
		self.currentgroup = 'loan'

	def deleteType(self):
		a = self.transaction_types[self.currentgroup].pop(self.transaction_types[self.currentgroup].index(self.listWidget.currentItem().text()))
		with open('transaction_types.json', 'w', encoding='utf-8') as transaction_types_file:
			json.dump(self.transaction_types, transaction_types_file)
		if self.currentgroup == 'reciept': 
			self.showReciepts()
		elif self.currentgroup == 'spend':
			self.showSpends()
		elif self.currentgroup == 'borrow':
			self.showBorrows()
		elif self.currentgroup == 'loan':
			self.showLoans()

	def addType(self):
		i, okBtnPressed = QInputDialog.getText(
			self, "Добавление категории", "Введите название новой категории")
		if okBtnPressed:
			self.transaction_types[self.currentgroup].append(i)
			with open('transaction_types.json', 'w', encoding='utf-8') as transaction_types_file:
				json.dump(self.transaction_types, transaction_types_file)
		if self.currentgroup == 'reciept': 
			self.showReciepts()
		elif self.currentgroup == 'spend':
			self.showSpends()
		elif self.currentgroup == 'borrow':
			self.showBorrows()
		elif self.currentgroup == 'loan':
			self.showLoans()



app = QApplication(sys.argv)
ex = TypeSettingsWindow()
ex.show()
sys.exit(app.exec_())