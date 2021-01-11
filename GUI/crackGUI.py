from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk
from subprocess import call
from pathlib import Path

def openDialog():
     root.filepath = filedialog.askopenfilename(title="Select A File", filetype=(("compressed files","*.rar;*.zip"),("all files", "*.*")))
     filePath.configure(text = root.filepath)

def openDialog2():
     root.filepath = filedialog.askopenfilename(title="Select A File", filetype=(("text files","*.txt"),("all files", "*.*")))
     filePassPath.configure(text = root.filepath)

def startApp():
     Arg = list('123456')
     if myNotebook.tab(myNotebook.select(), "text") == "Tùy chỉnh mật khẩu":
          # Check path
          path = filePath.cget("text")
          if path == "":
               messagebox.showerror("Thông báo", "Chưa chọn đường dẫn file nén")
               return
          else:
               Arg[0] = path
          # Check length password
          try:
               if startNum.get() == "" and maxNum.get() == "":
                    Arg[1] = "noStartLength"
                    Arg[2] = "noMaxLength"
               else:
                    startLength = startNum.get()
                    maxLength = maxNum.get()
                    if int(startLength) > int(maxLength):
                         messagebox.showerror("Thông báo", "Số kí tự tối thiểu phải nhỏ hơn hoặc bằng số kí tự tối đa")
                         return
                    else:
                         Arg[1] = int(startNum.get())
                         Arg[2] = int(maxNum.get())
          except ValueError:
               messagebox.showerror("Thông báo", "Nhập dữ liệu kiểu số cho độ dài kí tự")
               return
          # Check type of password
          if typeOfPwd.get() == 1:
               if yesLower.get() == 0 and yesUpper.get() == 0 and yesNum.get() == 0 and yesSpec.get() == 0:
                    messagebox.showerror("Thông báo", "Chọn tối thiểu 1 loại kí tự")
                    return
               else:
                    Arg[3] = ""
                    if yesLower.get():
                         Arg[3] = Arg[3] + "abcdefghijklmnopqrstuvwxyz"
                    if yesUpper.get():
                         Arg[3] = Arg[3] + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    if yesNum.get():
                         Arg[3] = Arg[3] + "0123456789"
                    if yesSpec.get():
                         Arg[3] = Arg[3] + "HasSpecialCharacters"
          else:
               if customChar.get() == "":
                    messagebox.showerror("Thông báo", "Nhập bộ kí tự cho mật khẩu")
                    return
               else:
                    Arg[3] = customChar.get()
          # Check start and last of password
          if firstChar.get() == "":
               Arg[4] = "noFirstChar"
          else:
               Arg[4] = firstChar.get()
          if lastChar.get() == "":
               Arg[5] = "noLastChar"
          else:
               Arg[5] = lastChar.get()

          cmdline = "python crack.py -i " + Arg[0] + " " + str(Arg[1]) + " " + str(Arg[2]) + " " + str(Arg[3]) + " " + str(Arg[4]) + " " + str(Arg[5])
          print(cmdline)
          dir = Path().absolute()
          rc = call("start cmd /K " + cmdline, cwd=dir, shell=True)
     else:
          # Check path
          path = filePath.cget("text")
          if path == "":
               messagebox.showerror("Thông báo", "Chưa chọn đường dẫn file nén")
               return
          else:
               Arg[0] = path

          passpath = filePassPath.cget("text")
          if passpath == "":
               messagebox.showerror("Thông báo", "Chưa chọn đường dẫn file mật khẩu")
               return
          else:
               Arg[1] = passpath

          cmdline = "python crackwithfilepass.py -i " + Arg[0] + " " + Arg[1]
          print(cmdline)
          dir = Path().absolute()
          rc = call("start cmd /K " + cmdline, cwd=dir, shell=True)

def reloadResults():
     try:
          displayResult.configure(state="normal")
          f = open("crackpwdLog.txt", "r")
          text = f.read()
          displayResult.delete("1.0", END)
          displayResult.update()
          displayResult.insert(END, text)
          displayResult.see(END)
          f.close()
          displayResult.configure(state="disabled")
     except:
          pass

def closeApp():
     root.destroy()

def chooseTypeOfPassword():
     if typeOfPwd.get() == 2:
          lowerCheckBtn.configure(state="disabled")
          upperCheckBtn.configure(state="disabled")
          numCheckBtn.configure(state="disabled")
          specCheckBtn.configure(state="disabled")
          customChar.configure(state="normal")
     else:
          lowerCheckBtn.configure(state="normal")
          upperCheckBtn.configure(state="normal")
          numCheckBtn.configure(state="normal")
          specCheckBtn.configure(state="normal")
          customChar.configure(state="disabled")

root = Tk()

# Choose file
leftLabelFrame1 = LabelFrame(root, text="Chọn tập tin nén",  font=("Times New Roman", 14, "bold"))
leftLabelFrame1.place(x = 10, y = 0, width = 490, height = 70)
     # Button choose file
chooseFileBtn = Button(leftLabelFrame1, text="Mở", font=("Times New Roman", 10, "bold"), command=openDialog, bg = "cyan")
chooseFileBtn.place(x = 10, width = 50, height = 30)
     # Label display file path
filePathLabel = Label(leftLabelFrame1, text = "Đường dẫn:", font=("Times New Roman", 10, "bold"))
filePathLabel.place(x = 60, width = 80, height = 30)
filePath = Label(leftLabelFrame1, text = "", bg="cyan", anchor="w")
filePath.place(x = 140, width = 335, height = 30)

# My notebook
myNotebook = ttk.Notebook(root)
myNotebook.place(x = 10, y = 70, width = 490, height = 520)

# Custom password
leftLabelFrame2 = LabelFrame(myNotebook)
leftLabelFrame2.place(x = 10, y = 70, width = 490, height = 520)
myNotebook.add(leftLabelFrame2, text="Tùy chỉnh mật khẩu")
     # Label length of password
lenPwdLabel = Label(leftLabelFrame2, text = "Độ dài mật khẩu:", font=("Times New Roman", 10, "bold"))
lenPwdLabel.place(x = 10, height = 30)
          # From min
fromLenPwdLabel = Label(leftLabelFrame2, text = "Từ:", anchor = "w")
fromLenPwdLabel.place(x = 10, y = 30, width = 30, height = 30)
startNum = Entry(leftLabelFrame2, width = 5)
startNum.place(x = 40, y = 35)
          # To max
toLenPwdLabel = Label(leftLabelFrame2, text = "Đến:", anchor = "w")
toLenPwdLabel.place(x = 90, y = 30, width = 30, height = 30)
maxNum = Entry(leftLabelFrame2, width = 5)
maxNum.place(x = 130, y = 35)
UnitLabel = Label(leftLabelFrame2, text = "(Kí tự)", anchor = "w")
UnitLabel.place(x = 170, y = 30, width = 40, height = 30)

     # Choose type of password
PwdLabel = Label(leftLabelFrame2, text = "Mật khẩu gồm các kí tự:", font=("Times New Roman", 10, "bold"), anchor = "w")
PwdLabel.place(x = 10, y = 70, height = 30)

typeOfPwd = IntVar()
typeOfPwd.set(1)
typeOfPwdRadioBtn1 = Radiobutton(leftLabelFrame2, text="Kiểu 1: Gồm các loại kí tự:", variable=typeOfPwd, value = 1, anchor = "w", command = chooseTypeOfPassword)
typeOfPwdRadioBtn1.place(x = 20, y = 100, width = 200, height = 30)
typeOfPwdRadioBtn2 = Radiobutton(leftLabelFrame2, text="Kiểu 2: Gồm các kí tự:", variable=typeOfPwd, value = 2, anchor = "w", command = chooseTypeOfPassword)
typeOfPwdRadioBtn2.place(x = 20, y = 280, width = 200, height = 30)
          # In type 1:
yesLower = IntVar()
yesUpper = IntVar()
yesNum = IntVar()
yesSpec = IntVar()

type1LabelFrame = LabelFrame(leftLabelFrame2)
type1LabelFrame.place(x = 40, y = 130, width = 400, height = 140)

lowerCheckBtn = Checkbutton(type1LabelFrame, text="Chữ cái thường (abcdefghijklmnopqrstuvwxyz)", variable = yesLower, onvalue = 1, offvalue = 0)
lowerCheckBtn.deselect()
lowerCheckBtn.place(x = 10, y = 10)

upperCheckBtn = Checkbutton(type1LabelFrame, text="Chữ cái hoa (ABCDEFGHIJKLMNOPQRSTUVWXYZ)", variable = yesUpper, onvalue = 1, offvalue = 0)
upperCheckBtn.deselect()
upperCheckBtn.place(x = 10, y = 40)

numCheckBtn = Checkbutton(type1LabelFrame, text="Số (0123456789)", variable = yesNum, onvalue = 1, offvalue = 0)
numCheckBtn.deselect()
numCheckBtn.place(x = 10, y = 70)

specCheckBtn = Checkbutton(type1LabelFrame, text="Kí tự đặc biệt (!@#$%^&*()-_+=~`[]{}|\\:;\"'<>,.?/)", variable = yesSpec, onvalue = 1, offvalue = 0)
specCheckBtn.deselect()
specCheckBtn.place(x = 10, y = 100)
          #In type 2
customChar = Entry(leftLabelFrame2)
customChar.configure(state="disabled")
customChar.place(x = 40, y = 310, width = 400)
     # Guess start and last of password
firstLenPwdLabel = Label(leftLabelFrame2, text = "Nhóm kí tự đầu mật khẩu:", font=("Times New Roman", 10, "bold"), anchor = "w")
firstLenPwdLabel.place(x = 10, y = 350, height = 30)
firstChar = Entry(leftLabelFrame2)
firstChar.place(x = 40, y = 380, width = 400)

lastLenPwdLabel = Label(leftLabelFrame2, text = "Nhóm kí tự cuối mật khẩu:", font=("Times New Roman", 10, "bold"), anchor = "w")
lastLenPwdLabel.place(x = 10, y = 410, height = 30)
lastChar = Entry(leftLabelFrame2)
lastChar.place(x = 40, y = 440, width = 400)

# Get password from file
leftLabelFrame2_2 = LabelFrame(myNotebook)
leftLabelFrame2_2.place(x = 10, y = 70, width = 490, height = 520)
myNotebook.add(leftLabelFrame2_2, text = "Sử dụng tệp mật khẩu")

chooseFilePassLabel = Label(leftLabelFrame2_2, text = "Chọn tệp mật khẩu:", font=("Times New Roman", 10, "bold"))
chooseFilePassLabel.place(x = 10, height = 30)

chooseFilePassBtn = Button(leftLabelFrame2_2, text="Mở", font=("Times New Roman", 10, "bold"), command=openDialog2, bg = "cyan")
chooseFilePassBtn.place(x = 10, y = 30, width = 50, height = 30)
     # Label display file pass path
filePassPathLabel = Label(leftLabelFrame2_2, text = "Đường dẫn:", font=("Times New Roman", 10, "bold"))
filePassPathLabel.place(x = 60, y = 30, width = 80, height = 30)
filePassPath = Label(leftLabelFrame2_2, text = "", bg="cyan", anchor="w")
filePassPath.place(x = 140, y = 30, width = 335, height = 30)

# Result screen
rightLabelFrame = LabelFrame(root, text="Nhật ký dò tìm", font=("Times New Roman", 14, "bold"))
rightLabelFrame.place (x = 510, y = 0, width = 280, height = 590)

displayResult = scrolledtext.ScrolledText(rightLabelFrame, width = 40, height = 26, font = ("Times New Roman", 10))
displayResult.grid(column = 0, pady = 10, padx = 10)
try:
     f = open("crackpwdLog.txt", "r")
     text = f.read()
     displayResult.insert(END, text)
     f.close()
except:
     pass
displayResult.see(END)
displayResult.configure(state="disabled")

reloadBtn = Button(rightLabelFrame, text = "Làm mới", font=("Times New Roman", 10, "bold"), command=reloadResults, bg = "cyan")
reloadBtn.place(x = 10, y = 420, height = 30)

startBtn = Button(rightLabelFrame, text="Bắt đầu", font=("Times New Roman", 10, "bold"), command=startApp, bg = "cyan")
startBtn.place(x = 10, y = 480, width = 260, height = 30)
closeBtn = Button(rightLabelFrame, text="Thoát", font=("Times New Roman", 10, "bold"), command=closeApp, bg = "cyan")
closeBtn.place(x = 10, y = 520, width = 260, height = 30)

# Custom window
root.geometry ("800x600")
root.title("Ứng dụng dò tìm mật khẩu file nén - HaThanh")
root.resizable(width=False, height=False)
root.mainloop()