from constants import *
from neural_net import *
import pygame

# DRAW BOARD
def displayGoban(win):
    
    win.fill(BOARD_COLOUR)
    pygame.draw.rect(win, BLACK, (BOARD_OFFSET-1, BOARD_OFFSET-1, DIMENSIONS-SQUARE_SIZE+2, DIMENSIONS-SQUARE_SIZE+2), width = 1) # border square
    for row in range(BOARD_SIZE-1): # inside squares
        for col in range(BOARD_SIZE-1):
            pygame.draw.rect(win, BLACK, ((row*SQUARE_SIZE) +BOARD_OFFSET, (col*SQUARE_SIZE) +BOARD_OFFSET, SQUARE_SIZE, SQUARE_SIZE), width = 1)

def displayBoardstate(win, board):
    displayGoban(win)
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE):
            if board[col][row] == "X" or board[col][row] == "O": drawPiece(win, board[col][row], row, col)

def checkCaptures(board, turn):
    
    def countLiberties(board, col, row, alreadyChecked, group):
        alreadyChecked.append((col, row))
        group.append((col, row))
        colour = board[col][row]
        liberties = 0
        
        if col-1 >= 0:
            if (col-1, row) not in group:
                if board[col-1][row] == "+": liberties += 1
                elif board[col-1][row] == colour: liberties += countLiberties(board, col-1, row, alreadyChecked, group)
        if col+1 <= 8:
            if (col+1, row) not in group:
                if board[col+1][row] == "+": liberties += 1
                elif board[col+1][row] == colour: liberties += countLiberties(board, col+1, row, alreadyChecked, group)
        if row-1 >= 0:
            if (col, row-1) not in group:
                if board[col][row-1] == "+": liberties += 1
                elif board[col][row-1] == colour: liberties += countLiberties(board, col, row-1, alreadyChecked, group)
        if row+1 <= 8:
            if (col, row+1) not in group:
                if board[col][row+1] == "+": liberties += 1
                elif board[col][row+1] == colour: liberties += countLiberties(board, col, row+1, alreadyChecked, group)
        return liberties

    alreadyChecked = []
    toCapture = []
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE):
            if (col, row) not in alreadyChecked:
                alreadyChecked.append((col, row))
                if board[col][row] == "X" or board[col][row] == "O":
                    group = []
                    liberties = countLiberties(board, col, row, alreadyChecked, group)
                    if liberties == 0: toCapture.append(group)

    winner = "+"

    if len(toCapture) == 1: # only one group
        if board[toCapture[0][0][0]][toCapture[0][0][1]] == "X": winner = "O"
        elif board[toCapture[0][0][0]][toCapture[0][0][1]] == "O": winner = "X"
        for pos in toCapture[0]:
            board[pos[0]][pos[1]] = "+"
            if group[0] == "O": blackCaps += len(group)
            elif group[0] == "X": whiteCaps += len(group)
    
    elif len(toCapture) > 1: # multiple groups
        colours = []
        for group in toCapture:
            if board[group[0][0]][group[0][1]] not in colours: colours.append(board[group[0][0]][group[0][1]])

        if len(colours) == 1: # different groups of same colour
            if board[toCapture[0][0][0]][toCapture[0][0][1]] == "X": winner = "O"
            elif board[toCapture[0][0][0]][toCapture[0][0][1]] == "O": winner = "X"
            for group in toCapture:
                for pos in group:
                    board[pos[0]][pos[1]] = "+"
                    if group[0] == "O": blackCaps += len(group)
                    elif group[0] == "X": whiteCaps += len(group)
        
        else: # different groups of different colours
            for group in toCapture:
                c = key[turn%2]
                if board[group[0][0]][group[0][1]] == c:
                    toCapture.remove(group)
            if board[toCapture[0][0][0]][toCapture[0][0][1]] == "X": winner = "O"
            elif board[toCapture[0][0][0]][toCapture[0][0][1]] == "O": winner = "X"
            for group in toCapture:
                for pos in group:
                    board[pos[0]][pos[1]] = "+"
                    if group[0] == "O": blackCaps += len(group)
                    elif group[0] == "X": whiteCaps += len(group)
    
    return winner

def drawPiece(win, c, x, y):
    colour = BLACK if c == "X" else WHITE
    pygame.draw.circle(win, colour, (x * SQUARE_SIZE + BOARD_OFFSET, y * SQUARE_SIZE + BOARD_OFFSET), SQUARE_SIZE//2)

def show(board):
    for col in range(BOARD_SIZE):
        r = ""
        for row in range(BOARD_SIZE):
            r += f" {board[col][row]}"
        print(r)
    print()





def main():
    
    pygame.init()

    FPS = 60
    win = pygame.display.set_mode((DIMENSIONS, DIMENSIONS), pygame.RESIZABLE, pygame.SRCALPHA)
    pygame.display.set_caption("AI")

    run = True
    clock = pygame.time.Clock()
    displayGoban(win)
    board = [["+" for _ in range(BOARD_SIZE)] for _ in range (BOARD_SIZE)] # empty 2d array "board"
    board[4][5] = "X"
    board[5][4] = "X"
    board[4][4] = "O"
    board[5][5] = "O"
    global result
    result = ""
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
                    winner = checkCaptures(board, turn)

                    if winner != "+":
                        run = False
                        if winner == "X": result = "B+"
                        else: result = "W+"

                    turn += 1
                    addFlags(board, turn)

        displayBoardstate(win, board)
        
        if result != "":
            print(f"\n----------\nResult: {result}\n----------\n")

    pygame.quit()





def playGame(black, white, display):
    run = True
    board = [["+" for _ in range(BOARD_SIZE)] for _ in range (BOARD_SIZE)] # empty 2d array "board"
    board[4][5] = "X"
    board[5][4] = "X"
    board[4][4] = "O"
    board[5][5] = "O"
    global result
    result = ""
    turn = 0

    while run:

        if turn % 2 == 0: player = black # black's move
        elif turn % 2 == 1: player = white # white's move

        # GET THE MOVE
        valsOut = calculateOutput(boardStateToValsIn(board, turn), player)

        legal = False
        while legal == False:
            move = np.argmax(valsOut)
            xpos, ypos = move%9, move//9
            if board[ypos][xpos] == "+": legal = True
            else: valsOut[move] = -1
        
        board[ypos][xpos] = key[turn%2]
        
        if display: show(board)

        winner = checkCaptures(board, turn)
        if winner != "+":
            if winner == "X":
                if display: print(f"\n----------\nResult: B+\n----------\n")
                return black
            else:
                if display: print(f"\n----------\nResult: W+\n----------\n")
                return white

        turn += 1





def play(nets, display):
    winners = []
    for i in range(len(nets)//2):
        winner = playGame(nets[i*2], nets[(i*2)+1], display)
        winners.append(winner)
    return winners

print("\n\t\tGENERATING GEN 1\n")
nets = []
for _ in range(256):
    nets.append(randomiseNet(blankNet(), 1))
print("\n\t\tRUNNING\n")

genMax = 10
for gen in range(genMax):
    gen += 1
    print(f"\n\t\t\tGEN: {gen}\n")
    for _ in range(5):
        nets = play(nets, display=False)
        print("survived:", len(nets))
    print("\n\t\tFOUND 8 BEST\n")
    n = 0
    for i in range(8):
        n += 1
        print(f"\n\t\t\tCLONING NET {n}\n")
        for _ in range(31):
            nets.append(randomiseNet(nets[i], gen))
    print("\n\t\tCLONES MADE\n")
    shuffle(nets)

print(f"\n\t\t\tBEST OF GEN {gen}:\n")
for _ in range(8):
    nets = play(nets, display=False)
    print("survived:", len(nets))

nets.append(nets[0])
print(f"\n\t\t\tBEST OF GEN {gen} PLAYING ITSELF:\n")
play(nets, display=True)