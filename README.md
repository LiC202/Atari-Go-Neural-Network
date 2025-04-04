# Go-Neural-Network

Deep neural network for the game of Atari Go, v1

This is my first AI project, and it will be an AI that plays the game of Go on a 9x9 board (for some relative simplicity). I won't use any remotely neural network related libraries, it will all be done from scratch with maths alone.
The neural network will be trained using a genetic algorithm that pits 256 versions against each other in a tournament, where the best 16 will be cloned (and altered), and the rest discarded.

There are 3 components to the project:
- Game engine
- Neural network
- Genetic algorithm

Each of these will be broken down in detail here:

# Game-Engine

Main functions:
 - Carries out game logic
   - Maintains a board state
   - Receives new moves from the players
   - Calculates captures
   - Calculates illegal moves
   - Prevents illegal moves from being played
 - Displays the game in the console
 - Displays the game in a pygame window

My implementation of these rules has been almost perfect, meaning they work in general, but in some specific cases the game will bug, leading to empty spaces being incorrectly made illegal, and parts of groups being captured for no reason.
If anyone wants a problem to solve then I'd love to see if anyone could fix my `checkCaptures` and `addFlags` functions in `main.py`, so these bugs wouldn't happen.

The `checkCaptures` function works by checking each square in the board until one isn't empty, then it counts its liberties and does the same recursively for any neighbouring stone of the same colour.
All of these stones are kept track of, and by the time the board has been searched, every stone has been assigned to a group that either gets discarded, or saved to a list of groups `toCapture`.
Next, if there is only one group to capture then it captures it, if there are two then it checks whether they're the same or different colours, and then acts accordingly so as to allow placing a stone in a spot where it immediately becomes captured, so long as it can free up a liberty in the process.

# Neural-Net

The neural net is really what I was most excited to work on, closely followed by the gen alg.

Step one is defining my inputs and my outputs:
 - 81 inputs
   - One for each space on the board (-1 for opponent's colour, 1 for own colour)
 - 81 outputs
   - One for each space on the board
   - This would later be collapsed into one MOST preferred move

Next I had to decide how many hidden layers I would need, and how large they would be.
For this I decided on two hidden layers, each of 81 nodes.
This step is really always arbitrary, but maybe later with more experience I could say if this is too little or too much complexity.
Even with this number of nodes (324) there are 19683 different parameters for the neural net to play with.
I chose not to use biases on each node just because this is the first time I've ever done anything with AI or neural nets, and since the only library I'm using is numpy I thought best not make it too difficult for me to grasp (I'm now realising this really wouldn't've been hard to implement).
Writing this I'm half-way through the project and I'm realising that Go and neural nets with genetic algorithms was a terrible combination, the nature of there being changing number of available outputs (ideally, I don't know how NEAT works yet either) makes this very tough.
Next time I'll make a more complex network for a simpler game, that way I can learn the basics of neural nets easier.

Anyway...

I have an input matrix `valsIn`, multiplied by the first weight matrix `w1`, which I apply two `tanh` squashing functions to, and that gives me my first hidden layer `l1`.
Repeat using `l1` as the input, `w2` for the weights, and get an output of `l2`.
Finally I take `l2` and multiply it by `w3`, apply one sigmoid `tanh` function.
I understand that this process is usually done iteratively, but I'm really going into this blind so I'm happy to make mistakes like this, afterall at this stage all I want is for something to go from playing 100% randomly, to making a decision, however bad it is.
```
def calculateOutput(valsIn, net):
    
    l1 = tanhArray(tanhArray(np.matmul(net["w1"], valsIn))) # first hidden layer
    l2 = tanhArray(tanhArray(np.matmul([l1], net["w2"])))[0] # second hidden layer
    valsOut = tanhArray(np.matmul([l2], net["w3"]))[0] # output
    
    return valsOut
```
This returns an 81 item long list, where indeces 0-80 represent positions on the board.
All the values are some x, where 0 <= x <= 1. The greatest of these values will be the submitted move.

# Genetic-Algorithm

This is where it all goes wrong...

First of all, I should mention I did want to use a back-propagation, but this would require





















