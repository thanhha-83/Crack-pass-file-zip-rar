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
parser.add_argument('filepass', nargs='*', help='<file password>')

class Check:
	def __init__(self, Arg):
		self.type = None
		self.filepass = None

		if len(Arg) >= 2:
			self.getData(Arg)
		else:
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
		self.filepass = Arg[2]
	
	def getType(self, Arg):
		if os.path.splitext(Arg[1])[1] == ".rar" or os.path.splitext(Arg[1])[1]==".zip":
			self.type = os.path.splitext(Arg[1])[1]
		else:
			print ('Extension Error')
			parser.exit()

class Handler:
	def __init__(self, filepass, typeCompress):
		self.filepass = filepass
		self.location = sys.argv[2]
		self.type = typeCompress
		self.result = False
		self.GetFile()
		self.CheckFilePass()

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

	def Brute(self, password):
		try:
			if self.type == '.zip':
				tryPass = password.encode()
			else:
				tryPass = password
			print(tryPass)
			self.FileCrack.extractall(pwd=tryPass)
			self.result = True
		except:
			pass

	def CheckFilePass(self):
		self.start_time = time.process_time()
		with open(self.filepass, "r", encoding = "utf-8") as f:
			listPass = f.read().splitlines()
		for tryPass in listPass:
			self.Brute(tryPass)
			if self.result:
				print('Complete')
				print('Password:', tryPass)
				print('Time:', time.process_time() - self.start_time,'s')
				self.WriteToTxt(tryPass)
				self.Message(time.process_time() - self.start_time, tryPass)
				return
def main():
	check = Check(sys.argv[1:])
	args = parser.parse_args()
	rarfile.UNRAR_TOOL = "UnRAR.exe"
	Handling = Handler(check.filepass, check.type)

if __name__ == "__main__":
	main()
