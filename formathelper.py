# -*- coding: utf-8 -*-

def ourformateDate(string_with_date):
	date = string_with_date.split()[0].split('-')
	return str(date[2]) + '.' + str(date[1]) + '.' + str(date[0])
