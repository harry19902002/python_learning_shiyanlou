#!/usr/bin/env python3

import sys
from multiprocess import Process, Queue

staff_dict = {}

queue1 = Queue()
queue2 = Queue()

def read_standard(filename):
	number = []
	with open(filename,'r') as file:
		for line in file:
				pos = line.index('=')
				number.append(float(line[pos+2:]))
	return number

def get_staff_information(filename):
	with open(filename,'r') as file:
		content = file.readlines()
		for string in content:
			information = string.split(',')
			try:
				income = int(information[1])
				key = information[0]
			except ValueError:
				print("Parameter Error")
				return None
			staff_dict[key] = income
	return True

def calculate_shebao(income):
	jishuL = number[0]
	jishuH = number[1]
	insuranceSum = sum(number[2:])
	if income < jishuL:
		return jishuL * insuranceSum
	elif income < jishuH:
		return income * insuranceSum
	elif income >= jishuH:
		return jishuH *insuranceSum

def calculate_tax(incomeAfterShebao):
	incomeTax = incomeAfterShebao - 3500
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

def calculate(filename):
	number = read_standard(filename)


def output_file(filename):
	with open(filename,'w') as file:
		for staffNumber,incomeBeforeTax in staff_dict.items():
			shebao = calculate_shebao(incomeBeforeTax)
			incomeAfterShebao = incomeBeforeTax - shebao
			tax = calculate_tax(incomeAfterShebao)
			incomeAfterTax = incomeAfterShebao - tax
			shebao = format(shebao,".2f")
			tax = format(tax,".2f")
			incomeAfterTax = format(incomeAfterTax,".2f")
			file.write(staffNumber+','+str(incomeBeforeTax)+ ','+ shebao + ',' + tax + ',' + incomeAfterTax+'\n')

if __name__ == '__main__':
	staffFilename = sys.argv[4]
	outputFilename = sys.argv[6]
	standardFile = sys.argv[2]

	Process(target = get_staff_information).start()
	Process(target = calculate).start()
	Process(target = output_file).start()


	