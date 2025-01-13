from constants import *
import pygame

# DRAW BOARD
def displayGoban(win):
    
    win.fill(BOARD_COLOUR)
    pygame.draw.rect(win, BLACK, (BOARD_OFFSET-1, BOARD_OFFSET-1, WIDTH-SQUARE_SIZE+2, HEIGHT-SQUARE_SIZE+2), width = 1) # border square
    pygame.draw.circle(win, BLACK, (WIDTH//2, HEIGHT//2), DOT_RADIUS)# centre dot
    for row in range(ROWS-1): # inside squares
        for col in range(COLS-1):
            pygame.draw.rect(win, BLACK, ((row*SQUARE_SIZE) +BOARD_OFFSET, (col*SQUARE_SIZE) +BOARD_OFFSET, SQUARE_SIZE, SQUARE_SIZE), width = 1)

def displayBoardstate(win, board):
    displayGoban(win)
    for col in range(COLS):
        for row in range(ROWS):
            if board[col][row] == "X" or board[col][row] == "O": drawPiece(win, board[col][row], row, col)

def checkCaptures(board, turn):
    
    def countLiberties(board, col, row, already_checked, group):
        already_checked.append((col, row))
        group.append((col, row))
        colour = board[col][row]
        liberties = 0
        
        if col-1 >= 0:
            if (col-1, row) not in group:
                if board[col-1][row] == "+": liberties += 1
                elif board[col-1][row] == colour: liberties += countLiberties(board, col-1, row, already_checked, group)
        if col+1 <= 8:
            if (col+1, row) not in group:
                if board[col+1][row] == "+": liberties += 1
                elif board[col+1][row] == colour: liberties += countLiberties(board, col+1, row, already_checked, group)
        if row-1 >= 0:
            if (col, row-1) not in group:
                if board[col][row-1] == "+": liberties += 1
                elif board[col][row-1] == colour: liberties += countLiberties(board, col, row-1, already_checked, group)
        if row+1 <= 8:
            if (col, row+1) not in group:
                if board[col][row+1] == "+": liberties += 1
                elif board[col][row+1] == colour: liberties += countLiberties(board, col, row+1, already_checked, group)
        return liberties

    already_checked = []
    toCapture = []
    for col in range(COLS):
        for row in range(ROWS):
            if (col, row) not in already_checked:
                already_checked.append((col, row))
                if board[col][row] == "X" or board[col][row] == "O":
                    group = []
                    liberties = countLiberties(board, col, row, already_checked, group)
                    if liberties == 0: toCapture.append(group)

    if len(toCapture) == 1: # only one group
        for pos in toCapture[0]: board[pos[0]][pos[1]] = "+" if len(toCapture[0]) != 1 else "F"
    
    elif len(toCapture) > 1: # multiple groups
        colours = []
        for group in toCapture:
            if board[group[0][0]][group[0][1]] not in colours: colours.append(board[group[0][0]][group[0][1]])
        
        if len(colours) == 1: # different groups of same colour
            for group in toCapture:
                for pos in group: board[pos[0]][pos[1]] = "+" if len(group) != 1 else "F"
        
        else: # different groups of different colours
            for group in toCapture:
                c = key[turn%2]
                if board[group[0][0]][group[0][1]] == c:
                    toCapture.remove(group)
            for group in toCapture:
                for pos in group: board[pos[0]][pos[1]] = "+" if len(group) != 1 else "F"

def drawPiece(win, c, x, y):
    colour = BLACK if c == "X" else WHITE
    pygame.draw.circle(win, colour, (x * SQUARE_SIZE + BOARD_OFFSET, y * SQUARE_SIZE + BOARD_OFFSET), SQUARE_SIZE//2)

def addFlags(board, turn): # flags empty squares that are NOT legal moves
    c = key[(turn)%2]
    newBoard = [row.copy() for row in board] # chatgpt helped here
    for col in range(COLS):
        for row in range(ROWS):
            if newBoard[col][row] == "+":
                newBoard[col][row] = c
                checkCaptures(newBoard, turn)

                old = sum(row.count(c) for row in board) # and here
                new = sum(row.count(c) for row in newBoard)
                if new <= old:
                    board[col][row] = "F"

                newBoard[col][row] = "+"

def removeFlags(board): # removes all flags
    for col in range(COLS):
        for row in range(ROWS):
            if board[col][row] == "F": board[col][row] = "+"

def show(board):
    for col in range(COLS):
        r = ""
        for row in range(ROWS):
            r += f" {board[col][row]}"
        print(r)
    print()


pygame.init()

FPS = 60
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SRCALPHA)
pygame.display.set_caption("AI")

def main():
    run = True
    clock = pygame.time.Clock()
    displayGoban(win)
    board = [["+" for _ in range(COLS)] for _ in range (ROWS)] # empty 2d array "board"
    turn = 0

    while run: # UPDATE
        clock.tick(FPS)
        pygame.display.update()

        for event in pygame.event.get(): # EVENTS

            if event.type == pygame.QUIT: # QUIT
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN: # CLICK
                pos = pygame.mouse.get_pos()
                xpos = pos[0]//SQUARE_SIZE
                ypos = pos[1]//SQUARE_SIZE

                if board[ypos][xpos] == "+": # only if the move is legal
                    
                    removeFlags(board)
                    board[ypos][xpos] = key[turn%2]
                    checkCaptures(board, turn)

                    turn += 1
                    addFlags(board, turn)
                    show(board)
            
        displayBoardstate(win, board)

    pygame.quit()

main()

# 405 nodes
# 26244 edges
# = total of 26649 values