import os

strpath = "/home/dohun/Documents/snapshots"
files = os.listdir(strpath)

for file in files:
    print(file)