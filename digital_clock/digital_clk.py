from tkinter import *
import time

clk=Tk()
clk.title('Clock')
clk.geometry('1350x700+0+0')
clk.config(bg='black')

def clock():
    h=time.strftime("%H")
    m=time.strftime("%M")
    s=time.strftime("%S")
    
    if int(h)>12 and int(m)>0:
        meridian_lbl.config(text="PM")
    if int(h)>12:
        h=str(int(int(h)-12))
    hr.config(text=h)
    min.config(text=m)
    sec.config(text=s)

    hr.after(100,clock)

hr=Label(clk,text="12",font=('Times 20 bold',75,'bold'),bg="#0875B7",fg='white')
hr.place(x=350,y=200,width=150,height=150)
hr_lbl=Label(clk,text="HOUR",font=('Times 20 bold',20,'bold'),bg="#0875B7",fg='white')
hr_lbl.place(x=350,y=360,width=150,height=50)

min=Label(clk,text="12",font=('Times 20 bold',75,'bold'),bg="#0875B7",fg='white')
min.place(x=530,y=200,width=150,height=150)
min_lbl=Label(clk,text="MINUTES",font=('Times 20 bold',20,'bold'),bg="#0875B7",fg='white')
min_lbl.place(x=530,y=360,width=150,height=50)

sec=Label(clk,text="12",font=('Times 20 bold',75,'bold'),bg="#0875B7",fg='white')
sec.place(x=710,y=200,width=150,height=150)
sec_lbl=Label(clk,text="SECONDS",font=('Times 20 bold',20,'bold'),bg="#0875B7",fg='white')
sec_lbl.place(x=710,y=360,width=150,height=50)

meridian_lbl=Label(clk,text="AM",font=('Times 20 bold',70,'bold'),bg="#9F0646",fg='white')
meridian_lbl.place(x=900,y=200,width=150,height=150)

state_lbl=Label(clk,text="MERIDIAN",font=('Times 20 bold',20,'bold'),bg="#9F0646",fg='white')
state_lbl.place(x=900,y=360,width=150,height=50)

clock()
clk.mainloop()