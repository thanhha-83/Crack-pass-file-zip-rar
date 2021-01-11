# Crack-pass-file-zip-rar
This is a simple tool to hekp you crack password of zip or rar files.

Author: Thanh Ha.

Reference source: https://github.com/mnismt/CompressedCrack.

## Requirements:
[Python 3.x](https://www.python.org/downloads/)

## Install:

```
apt-get -y install git
git clone https://github.com/thanhha-83/Crack-pass-file-zip-rar.git
cd ./Crack-pass-file-zip-rar
```

## Use in terminal
1. Crack with a set of characters
```
python crack.py -i INPUT [rules [rules ...]]

positional arguments:
  rules                 <min> <max> <character> <guessFirstLength> <guessLastLength>

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Insert the file path of compressed file
                        
```  
2. Crack with a file password (txt)
```
crackwithfilepass.py [-h] -i INPUT [filepass [filepass ...]]

positional arguments:
  filepass               <file password>

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Insert the file path of compressed file
                        
```  
## Use with GUI
```
It easy for you to use.
```
