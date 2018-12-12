# -*- coding: utf-8 -*-
import json
import datetime
import time


def ourformateDate(string_with_date):
	date = string_with_date.split()[0].split('-')
	return str(date[2]) + '.' + str(date[1]) + '.' + str(date[0])


def parser(QApplicationObject):
	QApplicationObject.lcdNumber.display(QApplicationObject.balance)
	QApplicationObject.lcdNumber_2.display(QApplicationObject.debt)

def boolean(string):
	if string in ['spend', 'loan']:
		return '-'
	elif string in ['reciept', 'borrow']:
		return '+'
	return None

def rememberAll():
	balance = 0
	debt = 0
	short_reports = []
	with open('inoutcome.json') as inoutcome:
		inoutcome_dictionary = json.loads(inoutcome.read())
	for transaction in inoutcome_dictionary:
		if inoutcome_dictionary[transaction]["type"] == 'reciept':
			balance += inoutcome_dictionary[transaction]["summ"]
		elif inoutcome_dictionary[transaction]["type"] == 'spend':
			balance -= inoutcome_dictionary[transaction]["summ"]
		elif inoutcome_dictionary[transaction]["type"] == 'borrow':
			balance += inoutcome_dictionary[transaction]["summ"]
			debt -= inoutcome_dictionary[transaction]["summ"]
		elif inoutcome_dictionary[transaction]["type"] == "loan":
			balance -= inoutcome_dictionary[transaction]["summ"]
			debt += inoutcome_dictionary[transaction]["summ"]

		short_reports.append(' '.join([' '.join(toDate(transaction).split()[:3]),
								 	   inoutcome_dictionary[transaction]["name"],
								 	   boolean(inoutcome_dictionary[transaction]["type"]),
								 	   str(inoutcome_dictionary[transaction]["summ"])]))
		# print(short_reports)
	return (balance, debt, short_reports[::-1])

def toDate(id_transaction):
	return str(time.ctime(int(round(float(id_transaction)))))
