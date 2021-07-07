from solver import gen_board, solve, valid
from settings import *
from btn_class import *
import pygame, sys
import time
pygame.font.init()

class Grid:
    def __init__(self, board, rows, cols, width, height):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.new_board = None
        self.selected = None
        self.solved = None
        
    def update_board(self):
        self.new_board = [[self.cubes[i][j].val for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].val == 0:
            self.cubes[row][col].set_val(val)
            self.update_board()
        
            if valid(self.new_board, val, (row, col)) and solve(self.new_board):
                return True
            else:
                self.cubes[row][col].set_val(0)
                self.cubes[row][col].set_temp(0)
                self.update_board()
                return False

    def sketch(self, temp):
        row, col = self.selected
        self.cubes[row][col].set_temp(temp)
    
    def draw(self, win):
        #Render cubes
        for i in range(self.rows):
            for j in range(self.cols):
                color = BLACK
                if self.board[i][j] != 0 and self.solved != 'wrong':
                        color = LOCKEDCOLOR
                self.cubes[i][j].draw(win, color)

        #Draw grid lines
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, BLACK, (0, i * cellSize), (self.width, i * cellSize), thick)
            pygame.draw.line(win, BLACK, (i * cellSize, 0), (i * cellSize, self.height), thick)
        
    def select(self, row, col):
        #Reset select state
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = row, col
    
    def clear(self):
        row, col = self.selected
        self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            x = pos[0] // cellSize
            y = pos[1] // cellSize
            return (int(y), int(x))
        else:
            return None
    
    def checkFilled(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].val == 0:
                    return False
        return True
    
    def solve(self, solved):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].set_val(solved[i][j])
        self.solved = 'solved'

    def reset(self):
        global END_TIME
        END_TIME = None
        self.selected = None
        self.solved = None
        self.new_board = None
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].set_val(self.board[i][j])
                self.cubes[i][j].set_temp(0)

class Cube:
    def __init__(self, val, row, col, width, height):
        self.val = val
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
    
    def draw(self, win, color=BLACK):
        font = pygame.font.SysFont("comicsans", 40)
        x = self.col * cellSize
        y = self.row * cellSize
        if self.temp != 0 and self.val == 0:
            text = font.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif self.val != 0:
            text = font.render(str(self.val), 1, color)
            win.blit(text, (x + (cellSize - text.get_width())//2, y + (cellSize - text.get_height())//2))
        if self.selected:
            pygame.draw.rect(win, RED, (x,y, cellSize, cellSize), 3)

    def set_temp(self, temp):
        self.temp = temp

    def set_val(self,val):
        self.val = val

def draw_all(win, Board, time, strikes, btns):
    global END_TIME
    over = None
    message = None
    font = pygame.font.SysFont("comicsans", 40)
    if Board.solved == 'solved':
        win.fill(LIGHTGREEN)
        if END_TIME is None:
            END_TIME = time
        text = font.render("Time: {}".format(format_time(END_TIME)), 1, BLACK)
        message = font.render("SOLVED", 1, BLACK) #Solved message
    elif Board.solved == 'wrong':
        win.fill(RED)
        if END_TIME is None:
            END_TIME = time
        over = font.render("GAME OVER!", 1, BLACK)
    else:
        win.fill(WHITE)
        text = font.render("Time: {}".format(format_time(time)), 1, BLACK)
    #SOLVED
    if message is not None:
        win.blit(message, (215, 561))
        win.blit(text, (380, 560))
    #GAMEOVER
    elif over is not None:
        win.blit(over, (185, 565))
    #Time
    else:
        win.blit(text, (205, 560))
    #Strikes
    text = font.render('X' * strikes, 1, RED)
    if strikes != 0:
        win.blit(text, (20, 560))
    #Draw buttons
    for btn in btns:
            btn.draw(win)
    #Draw grid and board
    Board.draw(win)

def load_btns(btns):
    btns.append(Btn(  50, 610, WIDTH//7, 40,
                                            color=BLUE,
                                            text="Reset"))
    btns.append(Btn(  227, 610, WIDTH//7, 40,
                                            color=GREEN,
                                            text="Solve"))
    btns.append(Btn(  408, 610, WIDTH//7, 40,
                                            color=YELLOW,
                                            text="New"))

def format_time(secs):
    sec = secs % 60
    minutes = secs // 60
    return (str(minutes) + ':' + str(sec))

def main():
    win = pygame.display.set_mode((540, 680))
    pygame.display.set_caption("SUDOKU")
    win.fill(WHITE)
    key = None
    run = True
    strikes = 0
    flag = 0
    board, solved = gen_board()
    Board = Grid(board, 9, 9, 540, 540)
    btns = []
    start = time.time()
    while run:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #On KeyPress
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_SPACE:
                    Board.solve(solved)
                    key = None
                if event.key == pygame.K_r:
                    key = None
                    Board.reset()
                if event.key == pygame.K_BACKSPACE:
                    Board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    if Board.selected is not None:
                        row, col = Board.selected
                        if Board.cubes[row][col].temp != 0:
                            if Board.place(Board.cubes[row][col].temp):
                                print("Yay")
                            else:
                                print("Nay")
                                strikes += 1
                                if strikes > 4:
                                    print("Game over")
                                    Board.solved = 'wrong'
                            key = None
                            if Board.checkFilled():
                                print("Game over")
                                run = False
                if event.key == pygame.K_n:
                    run = False
                    flag = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    btn.update(pos)
                clicked = Board.click(pos)
                if clicked and Board.solved != 'wrong':
                    Board.select(clicked[0], clicked[1])
                    key = None
                else:
                    for btn in btns:
                        if btn.highlighted:
                            if btn.text == 'Reset':
                                strikes = 0
                                start = time.time()
                                Board.reset()
                                key = None
                            elif btn.text == 'Solve':
                                Board.solve(solved)
                                key = None
                            elif btn.text == 'New':
                                run = False
                                flag = 1

            if Board.selected and key is not None:
                Board.sketch(key)
        
            
        draw_all(win, Board, play_time, strikes, btns)
        load_btns(btns)
        pygame.display.update()
    if flag == 1:
        del Board
        main()
            
                
main()
pygame.quit()              
