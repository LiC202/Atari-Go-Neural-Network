from constants import *
import numpy as np
from random import *

global e
e = 2.71828

def tanh(x):
    return ((e**x)-(e**(-x)))/((e**x)+(e**(-x)))

def tanhArray(x):
    
    numCols = np.size(x, 0)
    for i in range(numCols):
        y = x[i]
        x[i] = tanh(y)
    return x

def wiggle():
    return random()-0.5

def boardStateToValsIn(board, turn):
    if turn%2 == 0:                  # O = own colour
        for col in range(BOARD_SIZE):      # X = opponent's colour
            for row in range(BOARD_SIZE):
                if board[col][row] == "X": board[col][row] == "O"
                elif board[col][row] == "O": board[col][row] == "X"

    valsIn = np.zeros(162)

    boardState = ""
    for row in board:
        for val in row: boardState += val

    for i in range(len(boardState)):
        if boardState[i] == "+":
            valsIn[i*2] = 1
        if boardState[i] == "O":
            valsIn[(i*2)+1] = 1
        elif boardState[i] == "X":
            valsIn[(i*2)+1] = -1

    return valsIn

def valOutToBoardState(board, output, turn):
    colour = "X" if turn % 2 == 0 else "O"
    board[output//9][output%9] = colour
    return board

def blankNet():
    
    net = {
        "w1":np.zeros((81, 162)),
        "w2":np.zeros((81, 81)),
        "w3":np.zeros((81, 81))
    }
    return net

def randomiseNet(net, gen):
    
    for a in net:
        numRows, numCols = net[a].shape
        for i in range(numRows):
            for j in range(numCols):
                net[a][i][j] += tanh(wiggle()*(1/gen))

    return net

def calculateOutput(valsIn, net):
    
    l1 = tanhArray(tanhArray(np.matmul(net["w1"], valsIn))) # first hidden layer
    l2 = tanhArray(tanhArray(np.matmul([l1], net["w2"])))[0] # second hidden layer
    valsOut = tanhArray(np.matmul([l2], net["w3"]))[0] # output
    
    return valsOut