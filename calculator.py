#!/usr/bin/env python3

import sys

insurance_dict = {'endowment_insurance':0.08,
		'medical_insurance':0.02,
		'unemplotment_insurance':0.005,
		'injury_insurance':0,
		'maternity_insurance':0,
		'provient_found':0.06}

staff_dict = {}

def get_input():
	if len(sys.argv) == 1:
		print("Parameter Error")
		return None		
	for i in range(len(sys.argv)):
		if i == 1:
			continue
		print(sys.argv[i-1])
		inputList = sys.argv[i-1].split(':')
		try:
			return int(inputList[1])
		except ValueError:
			print("Parameter Error")
			return None
		staff_dict[inputList[0]] = inputList[1]
	return True

def calculate_insurance(income,insuranceSum):
	return income * insuranceSum

def calculate_tax(income,insurance):
	incomeTax = income - insurance - 3500
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

def calulate_finalIncome(income):
	insurance = calculate_insurance(income, insuranceSum)
	tax = calculate_tax(income, insurance)
	final_income = income - insurance - tax
	final_income = format(final_income,".2f")
	return final_income

if __name__ == '__main__':
	insuranceSum = 0
	for value in insurance_dict.values():
		insuranceSum += value
	if get_input() == True:
		for key,value in staff_dict:
			value = final_income(value)
			print("%d:%.2f" %(key,value))
	print(staff_dict)

