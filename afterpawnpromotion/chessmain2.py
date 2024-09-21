#this file is responsible for taking input from the user and presenting them on the board
import sys
import os
# Add the directory containing CHESSENGINE to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( r"D:\DOWNLOADS\CS50\Python\CHESSENGINE"), '.')))
import pygame as p
from CHESSENGINE import chessengine2 # type: ignore
width=height=512  #400 is another option
dimension=8
sq_size=height//dimension
maxfps=15 #for smooth animation
images={}
#initialise a global dictionary of images, it will be called only once
def loadimages():
    pieces=["bB","bK","bN","bp","bQ","bR","wB","wK","wN","wp","wQ","wR"]
    for piece in pieces:
        images[piece]=p.transform.scale(p.image.load(r"Chess pieces/"+piece+".png"), (sq_size,sq_size))   #when i copied the path \ this slash came but in this code we change it with / this
def main():
    p.init()
    screen=p.display.set_mode((width,height))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=chessengine2.gamestate()
    validmoves=gs.getvalidmoves()
    movemade=False   #flag variable for when a move is made

    loadimages() #do this only once before while loop
    running = True
    sqselected=()   #no square is selected, keep track of the last click of user(tuple:(row,col))
    playerclicks=[] #keep track of player clicks(two tuples:[(6,4),(4,4)])

    while running:
        for e in p.event.get():
            if e.type==p.QUIT:
                running=False
                #mouse handler
            elif e.type==p.MOUSEBUTTONDOWN:
                location=p.mouse.get_pos()   #(x,y) location of mouse
                col=location[0]//sq_size
                row=location[1]//sq_size
                if sqselected==(row,col):   #the user selected the same square twice, so it will not be considered as valid move
                    sqselected=() #deselect
                    playerclicks=[]  #clear player moves
                else:
                    sqselected=(row,col)    #2nd click
                    playerclicks.append(sqselected)   #append the both 1st and 2nd click in the player clicks
                if len(playerclicks)==2:  #after 2nd click
                    move=chessengine2.move(playerclicks[0],playerclicks[1],gs.board)
                    print(move.getchessnotations())
                    if move in validmoves:
                        gs.makemove(move)
                        movemade=True
                        sqselected=()   #reset user clicks
                        playerclicks=[]
                    else:
                        playerclicks=[sqselected]    # new change made to this code by adding this line of code to be able to select another piece because there was a bug by which if we select a piece and then select another piece, it is not moving
            #key handler
            elif e.type==p.KEYDOWN:
                if e.key==p.K_z:  #press z key
                    gs.undomove()
                    movemade=True
        if movemade:
            validmoves=gs.getvalidmoves()
            movemade=False

        
        drawgamestate(screen,gs)
        clock.tick(maxfps)
        p.display.flip()
'''
responsible for graphics within current game state
'''
def drawgamestate(screen,gs):
    drawboard(screen) #draw squares on the board
    #add in piece highlighting or move suggestion
    drawpieces(screen,gs.board)  #draw pieces on top of the squares


def drawboard(screen):
    #this function will be used to draw squares on the screen
    colors=[p.Color("white"),p.Color("grey")]
    for r in range(dimension):
        for c in range(dimension):
            color=colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))
def drawpieces(screen,board):
    for r in range(dimension):
        for c in range(dimension):
            piece=board[r][c]
            if piece !="--": #not empty spaces
                screen.blit(images[piece],p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))

if __name__=="__main__":
    main() 