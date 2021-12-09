"""
THis class is responsible for storing all the information about the currennt state of the chess game. It will also be responsible for determining the vaid moves of thee current state. it will also keep a move log
"""
class GameState():
    def __init__(self):
        # board is an 8x8 2d list, each element of the list has character
        # b, w is color
        # -- : no piece
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'] ]
        self.moveFuntions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                             'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves }
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False #checkMate: The King has no valid squares and it's in check => Bi chieu va het nuoc di => Thua
        self.staleMate = False #staleMate: The King has no valid squares and it's not in check => Het nuoc di, Khong bi chieu => Hoa
        self.enPassantPossible = () #coordinates for the square where en passant capture is possible
        self.enPassantPossibleLog = [self.enPassantPossible]
        #castle right
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightslog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        # castleRightslog luu tri cac currentCastlingRight truoc do phuc vu cho viec undo Move
    """
    Takes a Move as a parameter and executes it (this will not work for castling (nhap thanh), pawn promotion (phong Hau), and en-passsant" (tot an tot)
    """
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'  # di xong=> vi tri cu se rong
        self.board[move.endRow][move.endCol] = move.pieceMoved  # Vi tri moi se thay bang quan di chuyen
        self.moveLog.append(move)  # Luu tru cac o ma quan co da di => neu co undo thi di lai
        self.whiteToMove = not self.whiteToMove  # Ket thuc nuoc di cua 1 ben nguoi choi
        #update the King's location if it moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion change piece
        if move.isPawnPromotion:
            promotedPiece = input("Promote to Q, R, B, or N: ")
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece

        #en passant
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = '--'#capturing the pawn by en passant
            '''if not self.whiteToMove: #vi da doi truoc
                print("         => White Pawn actived", end="")
            else:
                print("         => Black Pawn actived", end="")
            print(" en-passant move")'''
        #update en passant varible
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advances => Chi khi con tot di len trong truong hop dac biet nhu the nay => moi co vi tri en passant co the danh cho quan Tot cua doi thu
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enPassantPossible = ()
        self.enPassantPossibleLog.append(self.enPassantPossible)
        #castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle move (King di sang ben phai, Rook di sang ben trai)=> King da di chuyen theo click => Cap nhat lai vi tri cu cua King va Rook
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] # moves the rook
                self.board[move.endRow][move.endCol + 1] = '--' #erase old rook, self.board[startRow, startCol] = '--'
            else: #queen side castle move #King di sang ben trai, Rook di sang ben phai
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2] # moves the rook
                self.board[move.endRow][move.endCol - 2] = '--'
            #print castling
            if not self.whiteToMove: #vi da doi truoc
                print("         => White Castling is actived")
            else:
                print("         => Black Castling is actived")


        #update castling rights : whenever it is a rook or a king move => Update moi khi xe hoac vua di chuyen
        self.updateCastleRights(move) # depend on Rule 1 of Castling
        # Them trang thai CurrentCastlingRight vao luu tru
        self.castleRightslog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    """
        Undo the last move mode
        """

    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # update the King's location if needed
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            # undo en passant move
            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = '--'  # leave lading square
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.enPassantPossibleLog.pop()
            self.enPassantPossible = self.enPassantPossibleLog[-1]

            # undo a 2 square pawnn advence
            '''if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()'''
            """
            if self.whiteToMove:
                print('    White ', end='')
            else:
                print('    Black ', end='')
            print('undo move')"""
            #undo Castling Rights
            self.castleRightslog.pop()
            self.currentCastlingRight = self.castleRightslog[-1]#set the current castle rights to the last one in the list
            #undo castle move => Ngoai viec xac dinh lai vi tri Vua va trang thai CastlingRight => xep lai Rook
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1] # Tra lai Rook cu
                    self.board[move.endRow][move.endCol - 1] = '--' # Xoa Rook moi (sau khi castling)
                else: #queen side
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1] # Tra lai Rook cu
                    self.board[move.endRow][move.endCol + 1] = '--' # Xoa Rook moi (sau khi castling)
            #ADD THESE
            self.checkMate = False
            self.staleMate = False
    """
    update the castle rights given the move
    """
    def updateCastleRights(self, move): # depend on Rule 1 of Castling
        if move.pieceCaptured == 'wR':#left rook ---> mat xe trang ben trai => khong the queenside Castling
            if move.endCol == 0: #left rook
                self.currentCastlingRight.wqs = False
            elif move.endCol == 7: #right rook  ---> mat xe trang ben phai => khong the kingside Castling
                self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endCol == 0: #left rook  ---> mat xe Den ben trai => khong the queenside Castling
                self.currentCastlingRight.bqs = False
            elif move.endCol == 7: #right rook ---> mat xe Den ben trai => khong the kingside Castling
                self.currentCastlingRight.bks = False

        #Neu King or Rook di chuyen => Khong the Castle tung ung nua
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRight.bks = False

    def checkForPinsAndChecks(self): # tra ve cac vi tri quan co check vua (enemy) , pin vua tuc: chan cho vua (ally) kem huong tu vua đen no va xem xem Vua co dang bi chieu khong
        pins = [] #squares where the allied pinned piece is and diretion pinned from => luu cac vi tri cua quan dong minh dang chan vua va huong tu vua ra quan ay
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        #check outboard from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () #reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':#Tranh truong hop con King bi chieu co the di chuyen khong hop le
                        if possiblePin == (): #1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: #2nd allied piece, so no pin or check possible in this direction => Neu co 2 con chan -> khong check huong nay nua
                            break

                    elif endPiece[0] == enemyColor: #quan dich enemy
                        type = endPiece[1]
                        #5 possiblities here in this comlpex conditional (tat ca tru con Ma (Knight)
                        #1. orthogonally away from king and piece is a rook
                        #2. diagonally away from king and piece is a bishop
                        #3. 1 square away diagonally from king and piece is a pawn
                        #4. any directions and piece is a queen
                        #5. any directions 1 square away and piece is a king (this necessary to prevent a king move to a square controlled by another king
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): #no piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: #piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else: #enemy piece not cheking
                            break
                else:
                    break #offboard
        #check for knightchecks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': #enemy Knight checking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return  inCheck, pins, checks


    """     
    Alll moves considering checks
    """
    def getValidMoves(self):
        moves = []
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                          self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if (len(self.checks) == 1):  # only one check, block check or move King => chi bi 1 quan chieu thi di chuyen Vua hoac chan cho Vua
                moves = self.getAllPossibleMoves()
                # to block a check => must move a piece into one of the squares between enemy piece and King
                # muon block a check => di chuyen mot con khac chan giua Vua va quan Enemy (dang chieu vua)
                check = self.checks[0]  # Check information (row, col, row_vector, col_vector) => Vi tri cua quan chieu vua va huong chieu
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]  # Enenmy piece causing the check
                validSquares = []  # squares that pieces can move to
                # If Knight, must capture Knight or move king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):  # Xet cac o co the tu vi tri vua den vi tri quan dang chieu Vua (tinh ca no)
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)  # check[2], check[3] are check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:  # neu da xet den ca Checking piece (tinh ca no)
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # go through backwards when you are removing from a list as iterating
                    if moves[i].pieceMoved[1] != 'K':  # move doesn't move King so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:  # move doesn't block check or capture checking piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else:  # not in check so all moves are fine
            moves = self.getAllPossibleMoves()
            if self.whiteToMove:
                self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
            else:
                self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                # TODO stalemate on repeate moves
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        self.currentCastlingRight = tempCastleRights
        return moves
        #for now we will noy worry about check

    """
    Determind if the current player is in check
    """
    def inCheck(self):#Check xem vua co bi chieu khong
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    """
    Determind if the enemy can attack the square r, c
    """
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponent's turn
        oopMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turn back
        for move in oopMoves:
            if move.endRow == r and move.endCol == c: #square is under attack
                return True
        return False
    """
    All moves without considedring checks
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of row
            for c in range(len(self.board[r])): #number of column
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    """
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                      #  print(moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                        """
                    self.moveFuntions[piece](r, c, moves) #calls the appropriate move function based on piece type
        return moves
    """
      Get all the pawn moves for the pawn located at row, col, and add these moves to the lis
      """
    def getPawnMoves(self, r, c, moves):
        """
        #New pawn Move
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            move_amount = -1
            startRow = 6
            enemyColor = "b"
            (kingRow, kingCol) = self.whiteKingLocation
        else:
            move_amount = 1
            startRow = 1
            enemyColor = "w"
            kingRow, kingCol = self.blackKingLocation

        if self.board[r + move_amount][c] == "--":  # 1 square pawn advance
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((r, c), (r + move_amount, c), self.board))
                if r == start_row and self.board[r + 2 * move_amount][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2 * move_amount, c), self.board))
        if c - 1 >= 0:  # capture to the left
            if not piecePinned or pinDirection == (move_amount, -1):
                if self.board[r + move_amount][c - 1][0] == enemyColor:
                    moves.append(Move((r, c), (r + move_amount, c - 1), self.board))
                if (r + move_amount, c - 1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(kingCol + 1, c - 1)
                            outside_range = range(c + 1, 8)
                        else:  # king right of the pawn
                            inside_range = range(kingCol - 1, c, -1)
                            outside_range = range(c - 2, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != "--":  # some piece beside en-passant pawn blocks
                                blockingPiece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + move_amount, c - 1), self.board, isEnPassantMove=True))
        if c + 1 <= 7:  # capture to the right
            if not piecePinned or pinDirection == (move_amount, +1):
                if self.board[r + move_amount][c + 1][0] == enemyColor:
                    moves.append(Move((r, c), (r + move_amount, c + 1), self.board))
                if (r + move_amount, c + 1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(kingCol + 1, c)
                            outside_range = range(c + 2, 8)
                        else:  # king right of the pawn
                            inside_range = range(kingCol - 1, c + 1, -1)
                            outside_range = range(c - 1, -1, -1)
                        for i in inside_range:
                            if self.board[r][i] != "--":  # some piece beside en-passant pawn blocks
                                blockingPiece = True
                        for i in outside_range:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + move_amount, c + 1), self.board, isEnpassantMove=True))

        """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == '--': #1 square on advanced
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r-1, c), self.board))
                    # Do con Tot Trang chi co the di len => Neu no o hang 6 thi chac chan la chua di => first move
                    if r == 6 and self.board[r-2][c] == '--': #2 squares for first move
                        moves.append(Move((r, c), (r-2, c), self.board))

            #captures
            if c-1 >= 0 and r > 0:
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture in the left
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r - 1, c - 1) == self.enPassantPossible:
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r-1, c-1), self.board, isenPassant = True))
            if c+1 <= 7 and r > 0:
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture in right
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r - 1, c + 1) == self.enPassantPossible:
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r-1, c+1), self.board, isenPassant = True))

        else: #black pawn move => chi di xuong
            if self.board[r+1][c] == '--': # 1 square on advanced
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == '--': #2 square on advanced
                        moves.append(Move((r, c), (r+2, c), self.board))
            #capture
            if c-1 >= 0 and r < 7:
                if self.board[r+1][c-1][0] == 'w': #eenmy piece to capture in the left
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r + 1, c - 1) == self.enPassantPossible:
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r+1, c-1), self.board, isenPassant = True))
            if c+1 <= 7 and r < 7:
                if self.board[r+1][c+1][0] == 'w': #enemy piece to capture in the right
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r + 1, c + 1) == self.enPassantPossible:
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r+1, c+1), self.board, isenPassant = True))
       #pawn promotion later

    """
      Get all the rook moves for the Rook located at row, col and add these moves to the list
      """
    def getRookMoves(self, r, c, moves): # Tai 1 vi tri cua Xe => xet 7 o con lai theo hang, cot( 4 huong, 14 o)
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, - 1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': #can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right
        if self.whiteToMove:
            enemyColor = 'b'
        else:
            enemyColor = 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7: #On board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--': # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #enemy piece vaid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: #friendly piece
                            break
                    else: #off board
                        break


    """
          Get all the rook moves for the Knight located at row, col and add these moves to the list
          """
    def getKnightMoves(self, r, c, moves):

        piecePinned = False
        for i in range(len(self.pins) - 1, - 1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1))
    #UPleft, UPright, upLEFT, upRIGHT,  downLEFT, downRIGHT, DOWNleft, DOWNright
        if self.whiteToMove:
            allyColor = 'w'
        else:
            allyColor = 'b'
        for a in knightMoves:
            endRow = r + a[0]
            endCol = c + a[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7: # On board
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: #(not ally piece <=> empty piece or enemy piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    """
          Get all the rook moves for the Bishop located at row, col and add these moves to the list
          """
    def getBishopMoves(self, r, c, moves, endRow=None): # Tuong, gan nhu xe, cung xet 4 huong
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #(r,c)
                    #, (up-left), (up-right), (down-left), (down-right)
        if self.whiteToMove:
            enemyColor = 'b'
        else:
            enemyColor = 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7: # on boar
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: # bao gom ca dieu kien la enemy va empty
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: #friendly piece invalid (Co quan minh can => khong di duoc)
                            break
                else: #off board
                    break


    """
          Get all the Queen moves for the Queen located at row, col and add these moves to the list
          """
    def getQueenMoves(self, r, c, moves):
        # Queen = Rook + Bshop
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    """
          Get all the rook moves for the King located at row, col and add these moves to the list
          """
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        if self.whiteToMove:
            allyColor = 'w'
        else:
            allyColor = 'b'
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7: #ON board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # gap enemy or empty
                    # place kig on end square and check for checks
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    #place king back on original location
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
        #self.getCastleMoves(r, c, moves)

    """
    Generate all valid castle moves for the king at (r, c) and ndd them to the list of move
    """
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):# Rule 2 of Castling
            return # can't castle while we are in check
        if (self.whiteToMove and self.currentCastlingRight.wks) \
                or (not self.whiteToMove and self.currentCastlingRight.bks): # depend on Rule 1 of Castleing
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) \
                or (not self.whiteToMove and self.currentCastlingRight.bqs): # depend on Rule 1 of Castleing
            self.getQueensideCastleMoves(r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':#Rule 4 of Castling
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):#Rule 3 of Castling
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove = True))
    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove = True))
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        #white king state, black king state, white queen statem black queen state => True Khi nào??

class Move():
    # Map( dictionary) : keys to value => key : value

    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
                   '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: u for u, v in ranksToRows.items()}
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: u for u, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isenPassant = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol] #VI tri ban dau di chuyen => nguon
        self.pieceCaptured = board[self.endRow][self.endCol] # Vi tri se di chuyen toi => Dich

        #pawn promotion
        # self.promotionChoice = 'Q'
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
            self.isPawnPromotion = True
        else:
            self.isPawnPromotion = False
        #en passant
        self.isEnPassantMove = isenPassant
        if self.isEnPassantMove:
            if self.pieceMoved[0] == 'w':
                self.pieceCaptured = 'bp'
            elif self.pieceMoved[0] == 'b':
                self.pieceCaptured = 'wp'

        #castle move
        self.isCastleMove = isCastleMove

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #=> Hash function : moveid
       # print(self.moveID)

    """
    Overriding the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    #overriding the str() funtion
    def __str__(self):
        #castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
