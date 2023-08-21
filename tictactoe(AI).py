import sys,copy,pygame
import numpy as np

WIDTH=550
HEIGHT=550
BG_COLOR="BLACK"
ROWS=3
COLS=3
LINE_COLOR="WHITE"
SQ_SIZE=WIDTH//COLS
LINE_WIDTH=10
RADIUS=SQ_SIZE//4
C_WIDTH=15
OFFSET=50

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("TIC TAC TOE")
screen.fill(BG_COLOR)

class Board:
    
    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))
        self.empty_sqrs=self.squares
        self.marked_sqrs=0
    
    def mark_square(self,row,col,player):
        self.squares[row][col] = player
        self.marked_sqrs+=1

    def empty_sq(self,row,col):
        return self.squares[row][col]==0

    def isFull(self):
        return self.marked_sqrs==9
    
    def isEmpty(self):
        return self.marked_sqrs==0
    
    def get_empty_squares(self):
        empty_squares=[]
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sq(row,col):
                    empty_squares.append((row,col))
        return empty_squares
    
    def final_State(self,show=False):
        #vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    iPos=(col*SQ_SIZE+SQ_SIZE//2, 20)
                    fPos=(col*SQ_SIZE+SQ_SIZE//2, HEIGHT-20)
                    pygame.draw.line(screen,"White",iPos,fPos,20)
                return self.squares[0][col]
        #horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    iPos=(20,row*SQ_SIZE+SQ_SIZE//2)
                    fPos=(WIDTH-20,row*SQ_SIZE+SQ_SIZE//2)
                    pygame.draw.line(screen,"White",iPos,fPos,20)
                return self.squares[row][0]
        #diagonals
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] !=0:
            if show:
                iPos=(20,20)
                fPos=(WIDTH-20,HEIGHT-20)
                pygame.draw.line(screen,"White",iPos,fPos,20)
            return self.squares[1][1]
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] !=0:
            if show:
                iPos=(20,HEIGHT-20)
                fPos=(WIDTH-20,20)
                pygame.draw.line(screen,"White",iPos,fPos,20)
            return self.squares[1][1]

        #no win state
        return 0

class Ai:
    def __init__(self,player=2):
        self.player=player

    def minimax(self,board,maximising):
        
        case = board.final_State()
        
        if case==1:
            return 1, None
        
        if case==2:
            return -1, None
        
        elif board.isFull():
            return 0, None
        
        if maximising:
            max_eval = -2
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for (row,col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row,col,1)
                eval = self.minimax(temp_board,False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row,col)
            
            return max_eval,best_move

        elif not maximising:
            min_eval = 2
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for (row,col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row,col,self.player)
                eval = self.minimax(temp_board,True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row,col)
            
            return min_eval,best_move

    def eval(self,game_board):
        eval,move = self.minimax(game_board,False)
        return move

class Game:
    
    def __init__(self):
        self.board = Board()
        self.player=1
        self.ai=Ai()
        self.running=True
        self.show_lines()
    
    def show_lines(self):
        screen.fill("Black")

        pygame.draw.line(screen,LINE_COLOR,(SQ_SIZE,0),(SQ_SIZE,HEIGHT),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(WIDTH-SQ_SIZE,0),(WIDTH-SQ_SIZE,HEIGHT),LINE_WIDTH)
        
        pygame.draw.line(screen,LINE_COLOR,(0,SQ_SIZE),(WIDTH,SQ_SIZE),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(0,HEIGHT-SQ_SIZE),(WIDTH,HEIGHT-SQ_SIZE),LINE_WIDTH)

    def next_turn(self):
        self.player = self.player%2+1 

    def draw_fig(self,row,col):
        if self.player == 1:
            strt_d=(col*SQ_SIZE+OFFSET,row*SQ_SIZE+OFFSET)
            end_d=(col*SQ_SIZE+SQ_SIZE-OFFSET,row*SQ_SIZE+SQ_SIZE-OFFSET)
            strt_a=(col*SQ_SIZE+OFFSET,row*SQ_SIZE+SQ_SIZE-OFFSET)
            end_a=(col*SQ_SIZE+SQ_SIZE-OFFSET,row*SQ_SIZE+OFFSET)
            pygame.draw.line(screen,"WHITE",strt_d,end_d,20)
            pygame.draw.line(screen,"WHITE",strt_a,end_a,20)
        elif self.player == 2:
            center = (col*SQ_SIZE+SQ_SIZE//2,row*SQ_SIZE+SQ_SIZE//2)
            pygame.draw.circle(screen,"WHITE",center,RADIUS,C_WIDTH)
        else:
            pass
    
    def isOver(self):
        return self.board.final_State(show=True) != 0 or self.board.isFull()

    def reset(self):
        self.__init__()

def main():

    game=Game()
    board=game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQ_SIZE
                col = pos[0] // SQ_SIZE

                if board.empty_sq(row,col)  and game.running:
                    board.mark_square(row,col,game.player)
                    game.draw_fig(row,col)
                    game.next_turn()

                    if game.isOver():
                        game.running=False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.reset()
                    board = game.board
                    ai = game.ai

        if ai.player == game.player and game.running:
            pygame.display.update()
            row,col = ai.eval(board)
            board.mark_square(row,col,ai.player) 
            game.draw_fig(row,col)
            game.next_turn() 
                
            if game.isOver():
                game.running=False

        pygame.display.update ()
        
main()