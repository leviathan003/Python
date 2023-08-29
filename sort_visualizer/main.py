import pygame
from tkinter import * 


class startPage():
    def __init__(self):
        self.root=Tk()
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry('300x400')
        self.root.config(bg='black')
        icon=PhotoImage(file='d:/CODE/Python/sort_visualizer/sort_visualizer_icon.png')
        self.root.iconphoto(False,icon)

        head=Label(self.root,text="Sorting Algorithm\nVisualizer",font='Arial 20 bold',bg='black',fg='white',relief='solid',borderwidth=3)
        head.pack(fill=X)
        
        button1=Button(self.root,text="Bubble Sort Visualizer",font='roboto 14 bold',bg='black',fg='white',relief='ridge',highlightbackground='yellow',highlightthickness=3,command=lambda:self.sort_Visualwindow('Bubble Sort Visualizer'))
        button1.place(x=25,y=90,width=250)
        button2=Button(self.root,text="Selection Sort Visualizer",font='roboto 14 bold',bg='black',fg='white',relief='ridge',highlightbackground='yellow',highlightthickness=3,command=lambda:self.sort_Visualwindow('Selection Sort Visualizer'))
        button2.place(x=25,y=150,width=250)
        button3=Button(self.root,text="Insertion Sort Visualizer",font='roboto 14 bold',bg='black',fg='white',relief='ridge',highlightbackground='yellow',highlightthickness=3,command=lambda:self.sort_Visualwindow('Insertion Sort Visualizer'))
        button3.place(x=25,y=210,width=250)
        button4=Button(self.root,text="Merge Sort Visualizer",font='roboto 14 bold',bg='black',fg='white',relief='ridge',highlightbackground='yellow',highlightthickness=3,command=lambda:self.sort_Visualwindow('Merge Sort Visualizer'))
        button4.place(x=25,y=270,width=250)
        button5=Button(self.root,text="Quick Sort Visualizer",font='roboto 14 bold',bg='black',fg='white',relief='ridge',highlightbackground='yellow',highlightthickness=3,command=lambda:self.sort_Visualwindow('Quick Sort Visualizer'))
        button5.place(x=25,y=330,width=250)
        
        self.root.mainloop()

    def show(self):
        for i in range(len(self.height)):
            pygame.draw.rect(self.win,(255,0,0),(self.x+30*i,self.y,self.width,self.height[i]))

    def sort_Visualwindow(self,name):
        pygame.init()
        
        icon=pygame.image.load('Uploaded/sort_visualizer/sort_visualizer_icon.png')
        pygame.display.set_icon(icon)

        self.win=pygame.display.set_mode((500,400))
        pygame.display.set_caption(name)

        self.x = 40
        self.y = 40
        self.width = 20
        self.height_original=[280, 260, 240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20]
        self.height = self.height_original
        run = True
        self.show()  

        
        while run:
            execute = False
            pygame.time.delay(10)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
        
            if keys[pygame.K_SPACE]:
                execute = True
        
            if execute == False:
                self.win.fill((0,0,0))
                self.show()
                pygame.display.update()

            else:
                if name=='Bubble Sort Visualizer':
                    self.bubble_sort()

                elif name=='Selection Sort Visualizer':
                    self.selection_sort()

                elif name=='Insertion Sort Visualizer':
                    self.insertion_sort()

                elif name=='Merge Sort Visualizer':
                    self.merge_sort()

                elif name=='Quick Sort Visualizer':
                    self.quick_sort()

        pygame.quit()    

    def disp_sorting(self):
        self.win.fill((0,0,0))
        self.show()
        pygame.time.delay(120)
        pygame.display.update()


    def bubble_sort(self):
        for i in range(len(self.height)-1):
            for j in range(len(self.height)-i-1):
                if self.height[j]>self.height[j+1]:
                    t = self.height[j]
                    self.height[j] = self.height[j+1]
                    self.height[j+1] = t
            
            self.disp_sorting()


    def selection_sort(self):
        for i in range(len(self.height)-1):
            min = i
            for j in range(i+1,len(self.height)):
                if self.height[j] < self.height[min]:
                    min = j


            t = self.height[i]
            self.height[i] = self.height[min]
            self.height[min] = t
            
            self.disp_sorting()


    def insertion_sort(self):
        for i in range(1,len(self.height)):
            key=self.height[i]
            j=i-1

            while j >= 0 and self.height[j] > key:
                self.height[j+1] = self.height[j]
                j = j-1

            self.height[j+1] = key

            self.disp_sorting()


    def merge_sort(self):
        self.merge_sort_recursion(0,len(self.height)-1)
        
    def merge_sort_recursion(self,l,r):
        if l < r:
            m = l+(r-l)//2
        else:
            return
        
        self.merge_sort_recursion(l,m)
        self.merge_sort_recursion(m+1,r)
        self.merge_sorted_arrays(l,m,r)
        
    def merge_sorted_arrays(self,l,m,r):
        n1 = m-l+1
        n2 = r-m

        L = [0] * (n1)
        R = [0] * (n2)

        for i in range(0,n1):
            L[i] = self.height[l+i]

        for j in range(0,n2):
            R[j] = self.height[m+1+j]

        i=0
        j=0
        k=l

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                self.height[k] = L[i]
                i += 1
            else:
                self.height[k] = R[j]
                j += 1
            k += 1

            self.disp_sorting()
  

        while i < n1:
            self.height[k] = L[i]
            i += 1
            k += 1
        
            self.disp_sorting()

        while j < n2:
            self.height[k] = R[j]
            j += 1
            k += 1

            self.disp_sorting()


    def quick_sort(self):
        self.quick_sort_recursion(0,len(self.height)-1)

    def quick_sort_recursion(self,l,r):
        if l < r:
            p = self.partition(l,r)
            self.quick_sort_recursion(l,p-1)
            self.quick_sort_recursion(p+1,r)

    def partition(self,l,r):
        pivot = self.height[r]
        i = l-1
        
        for j in range(l,r):
            if self.height[j] < pivot:
                i = i+1
                t = self.height[i]
                self.height[i] = self.height[j]
                self.height[j] = t
            
            self.disp_sorting()
 

        t = self.height[i+1]
        self.height[i+1] = self.height[r]
        self.height[r] = t

        self.disp_sorting()

        return i+1


obj=startPage()