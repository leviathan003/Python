import win32clipboard
import time
import threading

index=0
clips=["","","","",""]

def process_input():
    while True:
        choice=int(input())
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()    
        win32clipboard.SetClipboardText(clips[choice],win32clipboard.CF_TEXT)
        win32clipboard.CloseClipboard()

thread=threading.Thread(target=process_input)
thread.start()

while True:
    win32clipboard.OpenClipboard()
    data=win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    if data not in clips:
        clips[index]=data
        index+=1
        index%=5
        print(clips)
    time.sleep(1)