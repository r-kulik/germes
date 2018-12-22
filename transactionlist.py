# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton
import json
import sys
import time


class Example2(QWidget):

	def __init__(self):
		super().__init__()
		print('!1')
		self.setWindowTitle("Список транзакций")
		self.gui_init2()

	def gui_init2(self):
		transaction_list = []
		with open("inoutcome.json", 'r', encoding='utf-8') as transaction_file:
			transactions = json.loads(transaction_file.read())
		for transaction in transactions:
			transactions[transaction]["id"] = transaction
			transaction_list.append(transactions[transaction])
		# print(transaction_list)
		self.transaction_types = {'reciept': [], 'spend': [], 'borrow': [], 'loan': []}
		for transaction in transaction_list:
			self.transaction_types[transaction["type"]].append(transaction)
		#print(transaction_types)
		self.all_button = QPushButton("Все", self)
		self.all_button.setGeometry(10, 10, 150, 30)
		self.reciept_button = QPushButton("Доходы", self)
		self.reciept_button.setGeometry(160, 10, 150, 30)
		self.spend_button = QPushButton("Траты", self)
		self.spend_button.setGeometry(310, 10, 150, 30)
		self.borrow_button = QPushButton("Взятия в долг", self)
		self.borrow_button.setGeometry(460, 10, 150, 30)
		self.loan_button = QPushButton("Предоставления долга", self)
		self.loan_button.setGeometry(610, 10, 150, 30)
		self.all_button.clicked.connect(self.allShow)
		self.reciept_button.clicked.connect(self.recieptShow)
		self.spend_button.clicked.connect(self.spendShow)
		self.borrow_button.clicked.connect(self.borrowShow)
		self.loan_button.clicked.connect(self.loanShow)
		self.current_category = 'all'
		self.allShow()

	def allShow(self):
		showlist = []
		for key in self.transaction_types:
			showlist.extend(self.transaction_types[key])
		# print(showlist)
		for i in range(len(showlist)):
			transaction_time = time.ctime(float(showlist[i]["id"]))
			# print(transaction_time)
			transaction_type = showlist[i]["type"]
			transaction_name = showlist[i]["name"]
			transaction_balance = str(showlist[i]["summ"])
			if transaction_type == 'reciept':
				transaction_balance = '+' + transaction_balance
				transaction_debt = '0'
			elif transaction_type == 'spend':
				transaction_balance = '-' + transaction_balance
				transaction_debt = '0'
			elif transaction_type == 'borrow':
				transaction_balance = '+' + transaction_balance
				transaction_debt = '-' + str(showlist[i]["summ"])
			elif transaction_type == 'loan':
				transaction_balance = '-' + transaction_balance
				transaction_debt = '+' + str(showlist[i]["summ"])
			print(transaction_time, transaction_name, transaction_balance, transaction_debt)
			text = ' '.join([transaction_time, transaction_name, transaction_balance, transaction_debt])
			exec("self.label_" + str(i) + ' = QLabel(self)')
			exec("self.label_" + str(i) + '.setText(text)')
			exec("self.label_" + str(i) + '.show()')
			exec("self.label_" + str(i) + ".move(10, " +  str(40 + i * 20) + ")")







	def recieptShow(self):
		pass

	def spendShow(self):
		pass

	def borrowShow(self):
		pass
	
	def loanShow(self):
		pass


print('!4')
app = QApplication(sys.argv)
print('!3')
ex = Example2()
print('!2')
ex.show()
sys.exit(app.exec_())