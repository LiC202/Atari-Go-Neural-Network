from constants import *

def scoreGame(board, blackCaps, whiteCaps):
    
    blackPts = blackCaps
    whitePts = whiteCaps + 5.5

    def findNeighbours(board, col, row, alreadyChecked, group):
        alreadyChecked.append((col, row))
        group.append((col, row))
        neighbours = {
                    "X": 0,
                    "O": 0
                      }

        if col-1 >= 0:
            if (col-1, row) not in group:
                if board[col-1][row] == "+":
                    for c in ["X", "O"]: neighbours[c]+=findNeighbours(board, col-1, row, alreadyChecked, group)[c]
                else: neighbours[board[col-1][row]] += 1
        if col+1 <= 8:
            if (col+1, row) not in group:
                if board[col+1][row] == "+":
                    for c in ["X", "O"]: neighbours[c]+=findNeighbours(board, col+1, row, alreadyChecked, group)[c]
                else: neighbours[board[col+1][row]] += 1
        if row-1 >= 0:
            if (col, row-1) not in group:
                if board[col][row-1] == "+":
                    for c in ["X", "O"]: neighbours[c]+=findNeighbours(board, col, row-1, alreadyChecked, group)[c]
                else: neighbours[board[col][row-1]] += 1
        if row+1 <= 8:
            if (col, row+1) not in group:
                if board[col][row+1] == "+":
                    for c in ["X", "O"]: neighbours[c]+=findNeighbours(board, col, row+1, alreadyChecked, group)[c]
                else: neighbours[board[col][row+1]] += 1
        return neighbours
    
    alreadyChecked = []
    for col in range(COLS):
        for row in range(ROWS):
            group = []
            if (col, row) not in alreadyChecked:
                alreadyChecked.append((col, row))
                if board[col][row] == "+":
                    group = []
                    neighbours = findNeighbours(board, col, row, alreadyChecked, group)
                    if neighbours["X"] > 0 and neighbours["O"] > 0: # shared area
                        pass
                    elif neighbours["X"] > 0: # black points
                        blackPts += len(group)
                    elif neighbours["O"] > 0: # white points
                        whitePts += len(group)
            alreadyChecked.append((col, row))
        
    if blackPts > whitePts:
        print("Black wins.")
        #return "X"
    else: print("White wins.")
    #return "O"
    print(f"BLACK {blackPts} - {whitePts} WHITE")