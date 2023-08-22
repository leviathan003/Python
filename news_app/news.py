#b203968587ec4690a3cdd47c8cb1bba1

import requests
import io
from tkinter import *
import webbrowser
from urllib.request import urlopen
from PIL import ImageTk,Image

class news_App:
    def __init__(self):
        self.data=requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=b203968587ec4690a3cdd47c8cb1bba1').json()
        self.load_gui()
        self.loadnews_item(0)

    def load_gui(self):
        self.root=Tk()
        self.root.title('News App')
        self.root.geometry('350x600')
        self.root.resizable(0,0)
        self.root.configure(background='black')
    
    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def loadnews_item(self,index):
        self.clear()
        
        try:
            image=self.data['articles'][index]['urlToImage']
            img_data=urlopen(image).read()
            img= Image.open(io.BytesIO(img_data))
            photo = ImageTk.PhotoImage(img.resize((350,250)))

            img_label=Label(self.root,image=photo)
            img_label.pack()

        except:
            pass

        heading=Label(self.root,text=self.data['articles'][index]['title'],bg='black',fg='white',wraplength=350,justify='center')
        heading.pack(pady=(10,20))
        heading.config(font=('Arial',15))
        description=Label(self.root,text=self.data['articles'][index]['description'],bg='black',fg='white',wraplength=350,justify='center')
        description.pack(pady=(2,20))
        description.config(font=('Arial',12))
        
        frame=Frame(self.root,bg='black')
        frame.pack(expand=True,fill=BOTH)

        prev=Button(frame,text='Prev',width=16,height=3,command=lambda:self.loadnews_item(index-1))
        if index == 0:
            prev.config(state=DISABLED)    
            prev.pack(side=LEFT)
        else:
            prev.config(state=ACTIVE)    
            prev.pack(side=LEFT)

        readmore=Button(frame,text='Read More',width=16,height=3,command=lambda:self.open_link(self.data['articles'][index]['url']))
        readmore.pack(side=LEFT)

        next=Button(frame,text='Next',width=16,height=3,command=lambda: self.loadnews_item((index+1)%(len(self.data['articles'])-1)))
        next.pack(side=LEFT)
        
        self.root.mainloop()

    def open_link(self,url):
        webbrowser.open(url)

news=news_App()