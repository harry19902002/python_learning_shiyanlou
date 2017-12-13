#!/usr/bin/env python3

import sys

def get_input():
	if len(sys.argv) != 2:
		print("Parameter Error")
		return None
	try:
		return int(sys.argv[1])
	except ValueError:
		print("Parameter Error")
		return None

def calculate_tax(income):
	incomeTax = income - 3500
	if incomeTax <= 0:
		tax = 0
	elif incomeTax <= 1500:
		tax = incomeTax * 0.03
	elif  incomeTax <=4500:
		tax = incomeTax * 0.10 - 105
	elif incomeTax <= 9000:
		tax = incomeTax * 0.20 - 555
	elif incomeTax <= 35000:
		tax = incomeTax * 0.25 - 1005
	elif incomeTax <= 55000:
		tax = incomeTax * 0.30 - 2755
	elif incomeTax <= 80000:
		tax = incomeTax * 0.35 - 5505
	else:
		tax = incomeTax * 0.45 - 13505
	return tax

if __name__ == '__main__':
	income = get_input()
	if income != None:
		tax = calculate_tax(income)
		tax = format(tax,".2f")
		print(tax)

