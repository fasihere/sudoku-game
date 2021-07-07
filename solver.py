#Solve Sudoku (3x3)
import copy
from new_board import new_bo

def gen_board():
    board = new_bo()
    solved = copy.deepcopy(board)
    solve(solved)
    return board, solved

def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - - -')
        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(' | ', end="")
            if j == 8:
                print(bo[i][j])
            else:
                print(bo[i][j], end=" ")

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j) #row, column
    return None

def valid(bo, num, pos):

    #Check column
    for j in range(9):
        if bo[pos[0]][j] == num and pos[1] != j:
            return False

    #Check row
    for i in range(9):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3
    #Check grid
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True
    
def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
    for num in range(1, 10):
        if valid(bo,num,(row, col)):
            bo[row][col] = num

            if solve(bo):
                return True
            bo[row][col] = 0
    return False

gen_board()
gen_board()
#print('Before\n\n')
#print_board(bo)
#print('After\n\n')
#print_board(solved)
#print('\n')
