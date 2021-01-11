import zipfile
import rarfile
import os
import sys
from threading import Thread
import argparse
from itertools import product
import time
from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox
from tkinter import *
import csv
from datetime import datetime

parser = argparse.ArgumentParser(description='CompressedCrack', epilog='Use the -h for help')
parser.add_argument('-i','--input', help='Insert the file path of compressed file', required=True)
parser.add_argument('rules', nargs='*', help='<min> <max> <character> <guessFirstLength> <guessLastLength>')

class Check:
	def __init__(self, Arg):
		self.type = None
		self.rules = False
		self.startLength = None
		self.maxLength = None
		self.character = None
		self.guessFirstLength = None
		self.guessLastLength = None
		# Check Rules
		if len(Arg) >= 4:
			self.getData(Arg)
			self.rules = True
		elif len(Arg) == 0 or len(Arg) > 2:
			parser.print_help()
			parser.exit()
		# Check File Exist
		if (self.CheckFileExist(Arg)):
			self.getType(Arg)
		else:
			print ('No such file or directory: ', Arg[1])
			parser.exit()

	def CheckFileExist(self, Arg):
		if (os.path.isfile(Arg[1])):
			return True
		else:
			return False

	def getData(self, Arg):
		self.startLength = Arg[2]
		self.maxLength = Arg[3]
		if "HasSpecialCharacters" in Arg[4]:
			self.character = Arg[4].replace("HasSpecialCharacters", "!@#$%^&*()-_+=~`[]{}|\\:;\"'<>,.?/")
		else:
			self.character = Arg[4]
		self.guessFirstLength = Arg[5]
		self.guessLastLength = Arg[6]
	
	def getType(self, Arg):
		if os.path.splitext(Arg[1])[1] == ".rar" or os.path.splitext(Arg[1])[1]==".zip":
			self.type = os.path.splitext(Arg[1])[1]
		else:
			print ('Extension Error')
			parser.exit()

class Handler:
	def __init__(self, rules, typeCompress, startLength, maxLength, character, guessFirstLength, guessLastLength):
		self.rules = rules
		self.location = sys.argv[2]
		self.type = typeCompress
		if startLength != "noStartLength":
			self.startLength = int(startLength)
		else:
			self.startLength = startLength
		if maxLength != "noMaxLength":   
			self.maxLength = int(maxLength)
		self.character = character
		if guessFirstLength == "noFirstChar":
			self.guessFirstLength = ''
		else:
			self.guessFirstLength = guessFirstLength
		if guessLastLength == "noLastChar":
			self.guessLastLength = ''
		else:
			self.guessLastLength = guessLastLength
		self.result = False

		self.GetFile()
		self.CheckRules()

	def GetFile(self):
		# Khai báo file
		if self.type == '.zip':
			self.FileCrack = zipfile.ZipFile(self.location)
		else:
			self.FileCrack = rarfile.RarFile(self.location)

	def Message(self, time, password):
		root = Tk()
		root.overrideredirect(1)
		root.withdraw()
		messagebox.showinfo("Kết quả", "Time: {}s\nPassword: {}".format(time, password))
		root.destroy()

	def WriteToTxt(self, password):
		now = datetime.now()
		f = open("crackpwdLog.txt", "a")
		f.write(now.strftime("%d/%m/%Y %H:%M:%S") + "\n" + self.location + "\n" + password + "\n\n")
		f.close()

	def Brute(self,password):
		try:
			if self.type == '.zip':
				tryPass = password.encode()
			else:
				tryPass = password
			print(tryPass)
			self.FileCrack.extractall(pwd=tryPass)
			print('Complete')
			print('Time:',time.process_time() - self.start_time,'s')
			print('Password:',password)
			self.result = True
			self.WriteToTxt(password)
			self.Message(time.process_time() - self.start_time, password)
		except:
			pass

	def CheckRules(self):
		self.start_time = time.process_time()
		print('Cracking...')
		executor = ThreadPoolExecutor(max_workers=6)
		if self.startLength == "noStartLength":
			self.startLength = 1
			self.maxLength = 30
		for length in range(self.startLength, self.maxLength + 1):
			future = executor.submit(self.SendRequest, length, 0)
			future = executor.submit(self.SendRequest, length, -1)
			future = executor.submit(self.SendRequest, length, 1)
			if self.result:
				#executor.shutdown(wait=False)
				return

	def SendRequest(self, length, rev):
		#print('Working on ', length, 'and ', rev)
		if rev == 1:
			character = self.character[::-1]
		elif rev == 0:
			character = self.character
		else:
			character = self.character[int(len(self.character)/2):] + self.character[:int(len(self.character)/2)]
		listPass = product(character, repeat=length - len(self.guessFirstLength) - len(self.guessLastLength))
		for Pass in listPass:
			tryPass = self.guessFirstLength + ''.join(Pass) + self.guessLastLength
			self.Brute(tryPass)
			if self.result:
				#executor.shutdown(wait=False)
				return
		#print('Finished on ', length, 'and ', rev)
def main():
	check = Check(sys.argv[1:])
	args = parser.parse_args()
	rarfile.UNRAR_TOOL = "UnRAR.exe"
	Handling = Handler(check.rules, check.type, check.startLength, check.maxLength, check.character, check.guessFirstLength, check.guessLastLength)

if __name__ == "__main__":
	main()
