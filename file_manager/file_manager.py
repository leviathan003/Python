import os
import shutil

print("....This program sorts each file into folders based on its extension/type of file....")
path=input("Enter full path of directory to manage: ")

files=os.listdir(path)
for file in files:
    filename,extension=os.path.splitext(file)
    extension_new=extension[1:]
    fullpath=path+"\\"+extension_new

    if os.path.exists(fullpath):
        shutil.move(path+"\\"+file, path+'\\'+extension_new+'\\'+file)
    else:
        os.mkdir(fullpath)
        shutil.move(path+"\\"+file, path+'\\'+extension_new+'\\'+file)
