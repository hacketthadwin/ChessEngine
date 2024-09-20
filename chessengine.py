#this file is responsible for storing the information of the game and guess the next move on the basis of current state.it will also keep a move log

class gamestate():
    def __init__(self):
        #board is a 2d list that is list of lists where each element of list has 2 items row and columns
        #first character representing the color of the piece
        #second character representing the type of piece
        #'--' represents empty space
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.movefunctions={'p':self.getpawnmoves,'R':self.getrookmoves,'N':self.getknightmoves,
                            'B':self.getbishopmoves,'Q':self.getqueenmoves,'K':self.getkingmoves}
        self.whitetomove= True
        self.movelog=[]
        self.whitekinglocation=(7,4)
        self.blackkinglocation=(0,4)
        self.incheck=False
        self.checkmate = False
        self.stalemate = False
        self.pins=[]
        self.checks=[]
#takes a move as input and executes it(not work for castling, pawn promotion and en passante)
    def makemove(self,move):
        self.board[move.startrow][move.startcol]="--"
        self.board[move.endrow][move.endcol]=move.piecemoved
        self.movelog.append(move) #log the move so we can undo it later
        self.whitetomove= not self.whitetomove    #switch turns
        #update king's position
        if move.piecemoved=="wK":
            self.whitekinglocation=(move.endrow,move.endcol)
        elif move.piecemoved=="bK":
            self.blackkinglocation=(move.endrow,move.endcol)
             
#undo moves
    def undomove(self):
        if len(self.movelog)!=0:  #check if there is move present to undo or not
            move=self.movelog.pop()
            self.board[move.startrow][move.startcol]=move.piecemoved
            self.board[move.endrow][move.endcol]=move.piececaptured    #make the original position as move in move log
            self.whitetomove= not self.whitetomove  #switch turns back
            if move.piecemoved=="wK":
                self.whitekinglocation=(move.startrow,move.startcol)
            elif move.piecemoved=="bK":
                self.blackkinglocation=(move.startrow,move.startcol)
            self.checkmate = False
            self.stalemate = False
# all moves considering checks
    def getvalidmoves(self):
        moves=[]
        self.incheck,self.pins,self.checks=self.checkforpinsandchecks()
        if self.whitetomove:
            kingrow=self.whitekinglocation[0]
            kingcol=self.whitekinglocation[1]
        else:
            kingrow=self.blackkinglocation[0]
            kingcol=self.blackkinglocation[1]
        if self.incheck:
            if len(self.checks)==1:   #only 1 check then we can block check or move king
                moves=self.getallpossiblemoves()
                #to block a check, you must move a piece into one of the squares between enemy piece and king
                check=self.checks[0]  #check information
                checkrow=check[0]   #The row index of the piece that is giving the check
                checkcol=check[1]   #The column index of the piece that is giving the check
                piecechecking=self.board[checkrow][checkcol]   #enemy piece causing the check
                validsquares=[]   #squares that pieces can move to
                #if knight checks, then either capture the knight or move the queen, in other pieces,we can block the check
                if piecechecking[1]=='N':
                    validsquares=[(checkrow,checkcol)]   #if the knight is the one that is giving the check, then the only squares that piece can move to is only to capture the knight, so only valid square is position of the knight, otherwise move the king(this option is with any oppnent piece giving check, so we can handle this seperately)
                else:
                    for i in range(1,8):
                        validsquare=(kingrow+check[2]*i,kingcol+check[3]*i)   #check[2] and check[3] are the row and column of check direction
                        validsquares.append(validsquare)
                        if validsquare[0]==checkrow and validsquare[1]==checkcol: #once you get to piece end checks
                            break
                    #get rid of those moves that don't block check or move king
                    for i in range(len(moves)-1,-1,-1):
                        if moves[i].piecemoved[1]!='K':   #move doesn't move king, so the piece that is checking must be blocked or captured
                            if not(moves[i].endrow,moves[i].endcol) in validsquares:     #move doesn't block check or capture piece, so this move must be removed from the moves
                                moves.remove(moves[i])
            else:   #double check, so either move king
                self.getkingmoves(kingrow,kingcol,moves)
        else:   #not in check,so every move is fine
            moves=self.getallpossiblemoves()
        if len(moves)==0:
            if self.incheck:
                self.checkmate=True
                print("boom checkmate")
                return
            else:
                self.stalemate=True
                print("ah shit,stalemate")
                return
        else:
            self.checkmate=False
            self.stalemate=False
        return moves   
            



    def in_check(self):      #find if the king is in check or not
        if self.whitetomove:
            return self.squareunderattack(self.whitekinglocation[0],self.whitekinglocation[1])
        else:
            return self.squareunderattack(self.blackkinglocation[0],self.blackkinglocation[1])
        

    def squareunderattack(self,r,c):      #see if the square r,c is under attack or not
        self.whitetomove=not self.whitetomove
        oppmoves=self.getallpossiblemoves()
        self.whitetomove=not self.whitetomove
        for move in oppmoves:
            if (move.endrow==r) and (move.endcol==c):               
                return True
        return False
         
         
#all moves without considering checks
    def getallpossiblemoves(self):
        moves=[]      
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                if(turn=='w' and self.whitetomove) or (turn=='b' and not self.whitetomove):   #black or white anything
                    piece=self.board[r][c][1]
                    self.movefunctions[piece](r,c,moves)   #to get desired move from the different getpawnmoves,getrookmoves,getbishopmoves and all
        return moves
    def checkforpinsandchecks(self):
        pins=[]    #square pins and the direction it is pinned from
        checks=[]   #squares where enemy is applying a check
        incheck=False
        if self.whitetomove:
            enemycolor="b"
            allycolor='w'
            startrow=self.whitekinglocation[0]
            startcol=self.whitekinglocation[1]
        else:
            enemycolor="w"
            allycolor='b'
            startrow=self.blackkinglocation[0]
            startcol=self.blackkinglocation[1]
        #check outwards from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(8):
            direction=directions[j] 
            possiblepin=()   #reset possible pins
            for i in range(1,8):
                endrow=startrow+direction[0]*i
                endcol=startcol+direction[1]*i
                if 0<=endrow<=7 and 0<=endcol<=7:
                    endpiece=self.board[endrow][endcol]
                    if endpiece[0]==allycolor and endpiece[1]!='K':
                        if possiblepin==():   #only the first allied piece can be pinned, if two pieces comes in way, then it is not a pin
                            possiblepin=(endrow,endcol,direction[0],direction[1])
                        else:
                            break
                    elif endpiece[0]==enemycolor:
                        enemytype=endpiece[1]
                        # 5 possibilities in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and enemytype == "R") or (4 <= j <= 7 and enemytype == "B") or (i == 1 and enemytype == "p" and ((enemycolor == "w" and 6 <= j <= 7) or (enemycolor == "b" and 4 <= j <= 5))) or (enemytype == "Q") or (i == 1 and enemytype == "K"):
                            if possiblepin == ():  # no piece blocking, so check
                                incheck = True
                                checks.append((endrow, endcol, direction[0], direction[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possiblepin)
                                break
                        else:  # enemy piece not applying checks
                            break
                else:
                    break   #offboard    
               
         # check for knight checks
        knightmoves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knightmoves:
            endrow = startrow + move[0]
            endcol = startcol + move[1]
            if 0 <= endrow <= 7 and 0 <= endcol <= 7:
                endpiece = self.board[endrow][endcol]
                if endpiece[0] == enemycolor and endpiece[1] == "N":  # enemy knight attacking a king
                    incheck = True
                    checks.append((endrow, endcol, move[0], move[1]))
        return incheck, pins, checks                       
                        
 #get all the pawn moves for the pawn located at row, col and add these moves to the list
    def getpawnmoves(self,r,c,moves):
        piecepinned=False
        pindirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecepinned=True
                pindirection=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whitetomove:
            if self.board[r-1][c]=="--":
                if not piecepinned or pindirection ==(-1,0):
                    moves.append(move((r,c),(r-1,c),self.board))
                    if r==6 and self.board[r-2][c]=="--":
                        moves.append(move((r,c),(r-2,c),self.board))
            if c-1>=0:  #captures to the left
                if self.board[r-1][c-1][0]=='b':
                    if not piecepinned or pindirection==(-1,-1):
                        moves.append(move((r,c),(r-1,c-1),self.board))
            if c+1<=7:  #captures to the left
                if self.board[r-1][c+1][0]=='b':
                    if not piecepinned or pindirection==(-1,1):
                        moves.append(move((r,c),(r-1,c+1),self.board))
        else:
            if self.board[r+1][c]=="--":
                if not piecepinned or pindirection==(1,0):
                    moves.append(move((r,c),(r+1,c),self.board))
                    if r==1 and self.board[r+2][c]=="--":
                        moves.append(move((r,c),(r+2,c),self.board))
            if c-1>=0:  #captures to the left
                if self.board[r+1][c-1][0]=='w':
                    if not piecepinned or pindirection==(1,-1):
                        moves.append(move((r,c),(r+1,c-1),self.board))
            if c+1<=7:  #captures to the left
                if self.board[r+1][c+1][0]=='w':
                    if not piecepinned or pindirection==(1,1):
                        moves.append(move((r,c),(r+1,c+1),self.board))
            

    #get all the rook moves for the rook located at row,col and add these to the list
    def getrookmoves(self,r,c,moves):
        piecepinned=False
        pindirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecepinned=True
                pindirection=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        enemycolor = "b" if self.whitetomove else "w"
        for direction in directions:
            for i in range(1, 8):
                endrow = r + direction[0] * i
                endcol = c + direction[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:  # check within bounds
                    if not piecepinned or pindirection==direction or pindirection==(-direction[0],-direction[1]):
                        endpiece = self.board[endrow][endcol]
                        if endpiece == "--":  # empty space valid
                            moves.append(move((r, c), (endrow, endcol), self.board))
                        elif endpiece[0] == enemycolor:  # enemy piece valid
                            moves.append(move((r, c), (endrow, endcol), self.board))
                            break
                        else:  # friendly piece invalid
                            break
                else:  # out of bounds
                    break

    #get all the bishop moves for the bishop located at row,col ans add these to the list
    def getbishopmoves(self,r,c,moves):
        piecepinned=False
        pindirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecepinned=True
                pindirection=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemycolor = "b" if self.whitetomove else "w"
        for d in directions:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:  # check within bounds
                    if not piecepinned or pindirection==d or pindirection==(-d[0],-d[1]):
                        endpiece = self.board[endrow][endcol]
                        if endpiece == "--":  # empty space valid
                            moves.append(move((r, c), (endrow, endcol), self.board))
                        elif endpiece[0] == enemycolor:  # enemy piece valid
                            moves.append(move((r, c), (endrow, endcol), self.board))
                            break
                        else:  # friendly piece invalid
                            break
                else:  # out of bounds
                    break

    #get all the queen moves for the queen located at row,col and add these to the list
    def getqueenmoves(self,r,c,moves):
        self.getrookmoves(r, c, moves)
        self.getbishopmoves(r, c, moves)

    #get all the king moves for the king located at row,col and add these to the list
    def getkingmoves(self,r,c,moves):
        row_moves = [-1, -1, -1, 0, 0, 1, 1, 1]
        col_moves = [-1, 0, 1, -1, 1, -1, 0, 1]
        allycolor = "w" if self.whitetomove else "b"
        for i in range(8):
            endrow = r + row_moves[i]
            endcol = c + col_moves[i]
            if 0 <= endrow < 8 and 0 <= endcol < 8:  # within bounds
                endpiece = self.board[endrow][endcol]
                if endpiece[0] != allycolor:  # not an ally piece (empty or enemy)
                    if allycolor=='w':
                        self.whitekinglocation=(endrow,endcol)
                    else:
                        self.blackkinglocation=(endrow,endcol)
                    incheck,pins,checks=self.checkforpinsandchecks()
                    if not incheck:
                        moves.append(move((r,c),(endrow,endcol),self.board))
                    if allycolor=='w':
                        self.whitekinglocation=(r,c)
                    else:
                        self.blackkinglocation=(r,c)


    #get all the knight moves for the knight located at row,col and add these to the list
    def getknightmoves(self,r,c,moves):
        piecepinned=False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecepinned=True
                self.pins.remove(self.pins[i])
                break
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        allycolor = "w" if self.whitetomove else "b"
        for i in range(8):
            endrow = r + knight_moves[i][0]
            endcol = c + knight_moves[i][1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:  # within bounds
                if not piecepinned:
                    endpiece = self.board[endrow][endcol]
                    if endpiece[0] != allycolor:  # not an ally piece (empty or enemy)
                        moves.append(move((r, c), (endrow, endcol), self.board))
    

class move():
    #maps keys to values
    #key:values
    rankstorow={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowstoranks={v:k for k,v in rankstorow.items()}
    
    coltofile={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    filetocol={v:k for k,v in coltofile.items()}
    def __init__(self,startsq,endsq,board):
        self.startrow=startsq[0]
        self.startcol=startsq[1]
        self.endrow=endsq[0]
        self.endcol=endsq[1]
        self.piecemoved=board[self.startrow][self.startcol]
        self.piececaptured=board[self.endrow][self.endcol]
        self.moveid=1000*self.startrow+100*self.startcol+10*self.endrow+self.endcol
        print(self.moveid)

    #overriding the equals method because python don't actually able to connect the given position in (6,4) as e2
    def __eq__(self,other):
        if isinstance(other,move):
            return self.moveid==other.moveid
        return False

        
    def getchessnotations(self):
        #you can add this to make this like real chess notation
        return self.getrankfile(self.startrow,self.startcol)+self.getrankfile(self.endrow,self.endcol)
    def getrankfile(self,r,c):
        return self.filetocol[c]+self.rowstoranks[r]

        
        
