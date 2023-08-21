import tkinter
from tkinter import Button
from tkinter import Canvas,Label,PhotoImage
from PIL import ImageTk,Image

BUTTON_FONT="comicsans 60"
LINE_WIDTH=5

root=tkinter.Tk()
root.geometry("550x550+800+80")
root.config(bg="black")
root.title("Tic Tac Toe")
bg_img=ImageTk.PhotoImage(Image.open("Uploaded/tictactoe/TIC tAC TOE.png"))

class Player1:
    score=0
    play=True

class constant:
    count=9

class Player2:
    score=0
    play=False

def disp_winner(winner):
    win_label=Label(root,text=winner,font="Arial 20 bold",bg="black",fg='white')
    win_label.place(x=180,y=50)

def reset(grid_frame,reset_button):
    global GRID 
    GRID = ['0','1','2','3','4','5','6','7','8']
    reset_button.place_forget()

    constant.count=9
    win_label_hide=Label(root,font="Arial 20 bold",bg="black",fg='black')
    win_label_hide.place(x=180,y=50,width=200,height=40)
    grid_frame=Canvas(root,bg='#000000',border=0,relief='flat')
    grid_frame.place(x=85,y=130,width=380,height=380)
    Player1.play,Player2.play=True,False
    draw_grid(grid_frame,380,380)
    place_buttons(grid_frame)

def draw_grid(grid_frame,W,H):
    x,y=0,0
    for i in range(3):
        grid_frame.create_rectangle(0,y,W,y+127,outline='#ffffff',width=LINE_WIDTH)
        for j in range(3):
            grid_frame.create_rectangle(x,0,x+127,H,outline='#ffffff',width=LINE_WIDTH)
            x+=127
        y+=127

def turn_swap(x):
    if x==Player1.play:
        t=Player1.play
        Player1.play=Player2.play
        Player2.play=t
        return Player1.play,Player2.play

global GRID 
GRID = ['0','1','2','3','4','5','6','7','8']
def wincheck(value,index):
    GRID[index]=str(value)
    if (GRID[0]==GRID[1]==GRID[2]) or (GRID[3]==GRID[4]==GRID[5]) or (GRID[6]==GRID[7]==GRID[8]):
        return True
    elif (GRID[0]==GRID[3]==GRID[6]) or (GRID[1]==GRID[4]==GRID[7]) or (GRID[2]==GRID[5]==GRID[8]):
        return True
    elif (GRID[0]==GRID[4]==GRID[8]) or (GRID[2]==GRID[4]==GRID[6]):
        return True
    else:
        return False

def back_reset(grid_frame):
    back_button=Button(root,text="Back",font="Arial 13",bg='black',fg='white',relief="flat",activebackground="black",command=lambda:restart(back_button,reset_button))
    back_button.place(x=20,y=20)
    reset_button=Button(root,text="Reset",font="Arial 13",bg='black',fg='white',relief="flat",activebackground="black",command=lambda:reset(grid_frame,reset_button))
    reset_button.place(x=470,y=20)

def place_pos(instance,v,grid_frame):
    button=instance
    if Player1.play:
        button.config(text="X",font=BUTTON_FONT)
    else:
        button.config(text="O",font=BUTTON_FONT)
    
    button.config(state="disabled")
    
    winner=wincheck(button['text'],v)
    constant.count-=1
    if constant.count==0 and winner==False:
        disp_winner("Draw Game!!")
        back_reset(grid_frame)

    if winner ==True and Player1.play==True:
        disp_winner("Player-1 Wins!!")
        back_reset(grid_frame)
    elif winner==True and Player2.play==True:
        disp_winner("Player-2 Wins!!")
        back_reset(grid_frame)

    Player1.play,Player2.play=turn_swap(Player1.play)

def place_buttons(grid_frame):
    button_0=Button(grid_frame,text="",bg='#000000',fg='white',relief="flat",activebackground="#000000",command=lambda:place_pos(button_0,0,grid_frame))
    button_0.place(x=3,y=3,width=122,height=122)
    
    button_1=Button(grid_frame,text="",bg='#000000',fg='white',relief="flat",activebackground="#000000",command=lambda:place_pos(button_1,1,grid_frame))
    button_1.place(x=130,y=3,width=122,height=122)
    
    button_2=Button(grid_frame,text="",bg='#000000',fg='white',relief="flat",activebackground="#000000",command=lambda:place_pos(button_2,2,grid_frame))
    button_2.place(x=256,y=3,width=122,height=122)
    
    button_3=Button(grid_frame,text="",bg='#000000',relief="flat",fg='white',activebackground="#000000",command=lambda:place_pos(button_3,3,grid_frame))
    button_3.place(x=3,y=130,width=122,height=122)

    button_4=Button(grid_frame,text="",bg='#000000',relief="flat",fg='white',activebackground="#000000",command=lambda:place_pos(button_4,4,grid_frame))
    button_4.place(x=130,y=130,width=122,height=122)

    button_5=Button(grid_frame,text="",bg='#000000',relief="flat",fg='white',activebackground="#000000", command=lambda:place_pos(button_5,5,grid_frame))
    button_5.place(x=256,y=130,width=122,height=122)

    button_6=Button(grid_frame,text="",bg='#000000',relief="flat",fg='white',activebackground="#000000",command=lambda:place_pos(button_6,6,grid_frame))
    button_6.place(x=3,y=257,width=122,height=122)

    button_7=Button(grid_frame,text="",bg='#000000',relief="flat",fg='white',activebackground="#000000",command=lambda:place_pos(button_7,7,grid_frame))
    button_7.place(x=130,y=257,width=122,height=122)

    button_8=Button(grid_frame,text="",bg='#000000',relief="flat",fg='white',activebackground="#000000",command=lambda:place_pos(button_8,8,grid_frame))
    button_8.place(x=256,y=257,width=122,height=122)

def game_page():
    grid_frame=Canvas(root,bg='#000000',border=0,relief='flat')
    grid_frame.place(x=85,y=130,width=380,height=380)
    draw_grid(grid_frame,380,380)
    return grid_frame

def buttonmaker(grid):
    place_buttons(grid)

def gridmaker(play_game,label_bg,quit_button):
    label_bg.place_forget()
    play_game.place_forget()
    quit_button.place_forget()
    grid=game_page()
    buttonmaker(grid)

def restart(back_button,reset_button):
    global GRID 
    GRID = ['0','1','2','3','4','5','6','7','8']
    
    win_label_hide=Label(root,font="Arial 20 bold",bg="black")
    win_label_hide.place(x=180,y=50,width=200,height=40)

    back_button.place_forget()
    reset_button.place_forget()

    Player1.play,Player2.play=True,False
    constant.count=9
    label_bg_reset=Label(root,image=bg_img)
    label_bg_reset.place(x=0,y=0)

    play_game=Button(root,text="Play Game",font="Roboto 15 bold",relief="flat",background='black',fg='white',activebackground='black',activeforeground='white',command=lambda:gridmaker(play_game,label_bg_reset,quit_button))
    play_game.place(x=220,y=370)

    quit_button=Button(root,text="Quit",font="Roboto 15 bold",relief="flat",background='black',fg='white',activebackground='black',activeforeground='white',command=lambda:exit(0))
    quit_button.place(x=250,y=420)

def start():
    label_bg=Label(root,image=bg_img)
    label_bg.place(x=0,y=0)
    
    play_game=Button(root,text="Play Game",font="Roboto 15 bold",relief="flat",background='black',fg='white',activebackground='black',activeforeground='white',command=lambda:gridmaker(play_game,label_bg,quit_button))
    play_game.place(x=220,y=370)

    quit_button=Button(root,text="Quit",font="Roboto 15 bold",relief="flat",background='black',fg='white',activebackground='black',activeforeground='white',command=lambda:exit(0))
    quit_button.place(x=250,y=420)


start()

root.mainloop()