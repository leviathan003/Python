from tkinter import *
from tkinter import ttk
import requests

win=Tk()
win.title("Weather App")
win.geometry("500x500+600+0")
win.config(bg='dark blue')

label=Label(win,text="Python Weather App",font=("Times new roman",35,"bold"))
label.place(x=25,y=50,width=450)

list_locations=[
    "Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"
]
city_name=StringVar()

com=ttk.Combobox(win,font=("Arial",18,'bold'),values=list_locations,textvariable=city_name)
com.place(x=25,y=120,height=50,width=450)

def get_weather():
    key="de1d95a31be0a306bcdad02700984b7f"
    city=city_name.get()
    print(city)
    data=requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}")
    #print(data)
    weather_lbl_ans.config(text=data.json()['weather'][0]['main'])
    condition_lbl_ans.config(text=data.json()['weather'][0]['description'])
    temp_lbl_ans.config(text=str(int(data.json()['main']['temp']-273.15)))
    pressure_lbl_ans.config(text=str(data.json()['main']['pressure']))

weather_lbl=Label(win,text="Weather: ",font=("times new roman",20,'bold'),fg='white',bg='dark blue')
weather_lbl.place(x=25,y=260,height=24,width=150)
weather_lbl_ans=Label(win,text="",font=("times new roman",20,'bold'),fg='white',bg='dark blue')
weather_lbl_ans.place(x=200,y=260,height=25,width=100)

condition_lbl=Label(win,text="Condition: ",font=("times new roman",20,'bold'),fg='white',bg='dark blue')
condition_lbl.place(x=25,y=290,height=24,width=150)
condition_lbl_ans=Label(win,text="",font=("times new roman",14,'bold'),fg='white',bg='dark blue')
condition_lbl_ans.place(x=200,y=290,height=24,width=150)

temperature_lbl=Label(win,text="Temperature: ",font=("times new roman",20,'bold'),fg='white',bg='dark blue')
temperature_lbl.place(x=25,y=324,height=35,width=170)
temp_lbl_ans=Label(win,text="",font=("times new roman",20,'bold'),fg='white',bg='dark blue')
temp_lbl_ans.place(x=200,y=332,height=24,width=100)

pressure_lbl=Label(win,text="Pressure: ",font=("times new roman",20,'bold'),fg='white',bg='dark blue')
pressure_lbl.place(x=25,y=370,height=24,width=150)
pressure_lbl_ans=Label(win,text="",font=("times new roman",20,'bold'),fg='white',bg='dark blue')
pressure_lbl_ans.place(x=200,y=370,height=24,width=100)

button=Button(win,text='Get Weather',font=("Times new roman",20,'bold'),command=get_weather)
button.place(x=163,y=190)

win.mainloop()