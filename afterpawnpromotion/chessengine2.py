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
#takes a move as input and executes it(not work for castling, pawn promotion and en passante)
    def makemove(self,move):
        self.board[move.startrow][move.startcol]="--"
        self.board[move.endrow][move.endcol]=move.piecemoved
        self.movelog.append(move) #log the move so we can undo it later
        self.whitetomove= not self.whitetomove
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
# all moves considering checks
    def getvalidmoves(self):
        #1).generate all the possible moves
        moves=self.getallpossiblemoves()
        #2).for each move,make the move
        for i in range(len(moves)-1,-1,-1):
            self.makemove(moves[i])    # first switch           
            #3).generate all opponent's moves           
            #4).for each of your opponent's moves, see if they attack your king
            self.whitetomove=not self.whitetomove  #second switch because makemove function switch the turns
            if self.incheck():
                moves.remove(moves[i])   #5).if they do attack your king, not a valid move
            self.whitetomove=not self.whitetomove    #third switch
            self.undomove()     #fourth switch and also undo the move we made because typically we didn't made the move, we just found is this move valid or not
        if len(moves)==0:
            if self.incheck():
                self.checkmate=True
                print("boom checkmate")
                return
            else:
                self.stalemate=True
                print("ah shit,stalemate")
                return
        else:
            self.checkmate=True
            self.stalemate=True
        return moves   


    def incheck(self):      #find if the king is in check or not
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


 #get all the pawn moves for the pawn located at row, col and add these moves to the list
    def getpawnmoves(self,r,c,moves):
        if self.whitetomove:   #white pawn moves
            if self.board[r-1][c]=="--": #1 square pawn advanced
                moves.append(move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="--": # 2 square pawn advances
                    moves.append(move((r,c),(r-2,c),self.board))
                #capturing begins
            if c-1>=0:  #captures to the left
                if self.board[r-1][c-1][0]=='b': #black piece is there to capture
                    moves.append(move((r,c),(r-1,c-1),self.board))
            if c+1<=7:   #captures to the right
                if self.board[r-1][c+1][0]=='b': #black piece is there to capture
                    moves.append(move((r,c),(r-1,c+1),self.board))
        else: #black to move
            if self.board[r+1][c]=="--": #1 square pawn advanced
                moves.append(move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="--": # 2 square pawn advances
                    moves.append(move((r,c),(r+2,c),self.board))
                #capturing begins
            if c-1>=0:  #captures to the left
                if self.board[r+1][c-1][0]=='w': #white piece is there to capture
                    moves.append(move((r,c),(r+1,c-1),self.board))
            if c+1<=7:   #captures to the right
                if self.board[r+1][c+1][0]=='w': #white piece is there to capture
                    moves.append(move((r,c),(r+1,c+1),self.board))

    #get all the rook moves for the rook located at row,col and add these to the list
    def getrookmoves(self,r,c,moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        enemy_color = "b" if self.whitetomove else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # check within bounds
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # empty space valid
                        moves.append(move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # enemy piece valid
                        moves.append(move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # out of bounds
                    break

    #get all the bishop moves for the bishop located at row,col ans add these to the list
    def getbishopmoves(self,r,c,moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemy_color = "b" if self.whitetomove else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # check within bounds
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # empty space valid
                        moves.append(move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # enemy piece valid
                        moves.append(move((r, c), (end_row, end_col), self.board))
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
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        ally_color = "w" if self.whitetomove else "b"
        for i in range(8):
            end_row = r + king_moves[i][0]
            end_col = c + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:  # within bounds
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # not an ally piece (empty or enemy)
                    moves.append(move((r, c), (end_row, end_col), self.board))

    #get all the knight moves for the knight located at row,col and add these to the list
    def getknightmoves(self,r,c,moves):
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        ally_color = "w" if self.whitetomove else "b"
        for i in range(8):
            end_row = r + knight_moves[i][0]
            end_col = c + knight_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:  # within bounds
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # not an ally piece (empty or enemy)
                    moves.append(move((r, c), (end_row, end_col), self.board))
    

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

        
        
