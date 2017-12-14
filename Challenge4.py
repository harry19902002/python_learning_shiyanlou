#!/usr/bin/env python3

import sys
from multiprocessing import Process, Queue, Lock, Value

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

def get_staff_information(filename,lineNumber):
	with open(filename,'r') as file:
		content = file.readlines()
		lineNumber.value = len(content)
		for string in content:
			information = string.split(',')
			try:
				income = int(information[1])
				key = information[0]
				with lock1:
						queue1.put([key,income])
			except ValueError:
				print("Parameter Error")
				return None
	return True

def calculate_shebao(income, number):
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

def calculate(filename,lineNumber):
	number = read_standard(filename)
	while lineNumber.value == -1:
		pass
	for i in range(lineNumber.value):
		data = queue1.get()
		incomeBeforeTax = data[1]
		shebao = calculate_shebao(incomeBeforeTax, number)
		incomeAfterShebao = incomeBeforeTax - shebao
		tax = calculate_tax(incomeAfterShebao)
		incomeAfterTax = incomeAfterShebao - tax
		shebao = format(shebao,".2f")
		tax = format(tax,".2f")
		incomeAfterTax = format(incomeAfterTax,".2f")
		with lock2:
			queue2.put([data[0],str(incomeBeforeTax),shebao,tax,incomeAfterTax])

def output_file(filename,lineNumber):
	with open(filename,'w') as file:
		while lineNumber.value == -1:
			pass
		for i in range(lineNumber.value):
			data = queue2.get()
			for content in data:
				file.write(content + ',')

			file.write('\b\n')

if __name__ == '__main__':
	staffFilename = sys.argv[4]
	outputFilename = sys.argv[6]
	standardFile = sys.argv[2]

	lock1 = Lock()
	lock2 = Lock()

	lineNumber = Value('i',-1)

	Process(target = get_staff_information ,args = (staffFilename,lineNumber)).start()
	Process(target = calculate , args = (standardFile,lineNumber)).start()
	Process(target = output_file , args = (outputFilename,lineNumber)).start()


	