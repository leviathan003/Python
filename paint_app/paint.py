from tkinter import *
from tkinter import filedialog,messagebox,colorchooser
from PIL import Image,ImageDraw

WIDTH=500
HEIGHT=500
CENTER =WIDTH//2
WHITE=(255,255,255)

class PaintGUI:
    def __init__(self):
        self.root=Tk()
        self.root.title("Simple Paint Clone")
        self.brush_width=15
        self.current_color="#000000"

        self.cnv=Canvas(self.root,width=WIDTH-10,height=HEIGHT,bg='white')
        self.cnv.pack()

        self.cnv.bind("<B1-Motion>",self.paint)

        self.img=Image.new("RGB",(WIDTH,HEIGHT),WHITE)
        self.draw=ImageDraw.Draw(self.img)

        self.button_frme=Frame(self.root)
        self.button_frme.pack(fill=X)
        
        self.button_frme.columnconfigure(0,weight=1)
        self.button_frme.columnconfigure(1,weight=1)
        self.button_frme.columnconfigure(2,weight=1)

        self.clear_button=Button(self.button_frme,text="CLEAR",command=self.clear)
        self.clear_button.grid(row=0,column=1,sticky=W+E)

        self.save_button=Button(self.button_frme,text="SAVE",command=self.save)
        self.save_button.grid(row=0,column=2,sticky=W+E)

        self.bplus_button=Button(self.button_frme,text="B+",command=self.brush_plus)
        self.bplus_button.grid(row=0,column=0,sticky=W+E)

        self.bminus_button=Button(self.button_frme,text="B-",command=self.brush_minus)
        self.bminus_button.grid(row=1,column=0,sticky=W+E)

        self.colpick_button=Button(self.button_frme,text="COLOR PICKER",command=self.colpick)
        self.colpick_button.grid(row=1,column=1,sticky=W+E)

        self.root.protocol("WM_DELETE_WINDOW",self.on_close)
        self.root.attributes("-topmost",True)
        self.root.mainloop()

    def paint(self,event):
        x1,y1=(event.x -1),(event.y -1)
        x2,y2=(event.x +1),(event.y +1)
        
        self.cnv.create_rectangle(x1,y1,x2,y2,outline=self.current_color,width=self.brush_width)
        self.draw.rectangle([x1,y1,x2+self.brush_width,y2+self.brush_width],outline=self.current_color,fill=self.current_color,width=self.brush_width)

    def clear(self):
        self.cnv.delete("all")
        self.draw.rectangle([0,0,1000,1000],fill="white")

    def save(self):
        filename=filedialog.asksaveasfilename(initialfile="untitled.png",defaultextension="png",filetypes=[("PNG",".png"),("JPG",".jpg")])
        if filename!="":
            self.img.save(filename)

    def brush_plus(self):
        self.brush_width+=1
    
    def brush_minus(self):
        if self.brush_width <= 1:
            self.brush_width=1
        else:
            self.brush_width-=1 

    def colpick(self):
        _,self.current_color=colorchooser.askcolor(title="Choose a Color")

    def on_close(self):
        answer=messagebox.askyesnocancel("Quit","Do you want to save your work?",parent=self.root)
        if answer is not None:        
            if answer is True:
                self.save()
            self.root.destroy
            exit(0)


PaintGUI()