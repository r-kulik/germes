# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel
from main_ui import Ui_MainWindow
import json
import datetime
from formathelper import ourformateDate



class Example(QMainWindow, Ui_MainWindow):
	
	def __init__(self):
		current_version = '0.1'
		super().__init__()
		self.setupUi(self)
		self.setWindowTitle("Гермес - Финансовый помощник")
		self.label_4.setText(current_version)
		self.pushButton.clicked.connect(self.add_transaction)

	def add_transaction(self):
		with open("inoutcome.json") as inoutcome:
			a = inoutcome.read()
			inoutcome_dictionary = json.loads(a)
			# print(inoutcome_dictionary)
		print(inoutcome_dictionary)
		"""
		current_date = ourformateDate(str(datetime.datetime.now()))
		day_transactions = '\n'.join(list(map(str, inoutcome_dictionary[current_date])))
		print(day_transactions)
		"""
		




app = QApplication(sys.argv)
ex = Example()
ex.show()
sys.exit(app.exec_())
