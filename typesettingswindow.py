# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from typesettingswindow_ui import Ui_MainWindow as SettingsUi_MainWindow
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


	def showReciepts(self):

		self.listWidget.clear()
		self.listWidget.addItems(self.transaction_types["reciept"])

	def showSpends(self):
		self.listWidget.clear()
		self.listWidget.addItems(self.transaction_types["spend"])

	def showBorrows(self):
		pass

	def showLoans(self):
		pass

app = QApplication(sys.argv)
ex = TypeSettingsWindow()
ex.show()
sys.exit(app.exec_())