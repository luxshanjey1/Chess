"""
This is the main driver file. It will be responsible for handling user input and displaying the current GameState
"""

import pygame as p
from Chess import ChessEngine

p.init() #initialize game
WIDTH = HEIGHT = 512 #400 is another option
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations later on
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Note: we can access image by saying 'IMAGES['wp']'


'''
Main driver for the code. This will handle user input and updating the graphics
'''

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState() #calls ChessEngine initialize and create board and other variables
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made

    loadImages() #only do it once, befor the while loop
    running = True
    sqSelected = () #empty because no square is selected right now, this will keep track of the last click of the user (tuple: (row,col))
    playerClicks = [] #keep track of a player clicks (two tuples: [(6,4),(4,4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN: ############# add drag and drop feature later ###############
                location = p.mouse.get_pos() #(x,y) locaiton of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): # the user clicked the same square twice
                    sqSelected = () #deselect square
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append for both 1st and 2nd clicks
                if len(playerClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () #reset user clicks
                    playerClicks = []
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_u: #undo when 'u' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for all the graphics within current gamestate
'''
def drawGameState(screen ,gs):
    drawBoard(screen) #draw square on the board
    #add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) #draw pieces on to pof those squares

'''
Draw the squares on the board
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")] #change colors of squares
    for row in range(DIMENSION):
        for column in range (DIMENSION):
            color = colors[((row+column) % 2)] #odd parity is gray and even parity is white
            p.draw.rect(screen, color, p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__ == "__main__":
        main()

























