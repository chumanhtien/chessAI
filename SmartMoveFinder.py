import random

pieceScore = {"K" : 0, "Q" : 9, "R" : 5, "B" : 3, "N" : 3, "p" : 1}
knightScores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]
# [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
#                  [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
#                  [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
#                  [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
#                  [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
#                  [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
#                  [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
#                  [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishopScores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]
    # [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
    #              [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
    #              [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
    #              [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
    #              [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
    #              [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
    #              [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
    #              [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rookScores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]
    # [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
    #            [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
    #            [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    #            [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    #            [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    #            [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    #            [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    #            [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queenScores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]
#     [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
#                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
#                 [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
#                 [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
#                 [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
#                 [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
#                 [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
#                 [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]
pawnScores =  [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.5, 0.6, 0.6, 0.7, 0.7, 0.6, 0.6, 0.5],
               [0.2, 0.3, 0.3, 0.5, 0.5, 0.3, 0.3, 0.2],
               [0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.1],
               [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],
               [0.1, 0.1, 0.1, 0.0, 0.0, 0.1, 0.1, 0.1],
               [0, 0, 0, 0, 0, 0, 0, 0]]
piecePositionScores = {"wN": knightScores,
                         "bN": knightScores[::-1],
                         "wB": bishopScores,
                         "bB": bishopScores[::-1],
                         "wQ": queenScores,
                         "bQ": queenScores[::-1],
                         "wR": rookScores,
                         "bR": rookScores[::-1],
                         "wp": pawnScores,
                         "bp": pawnScores[::-1]
                        }
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3
def findRandomMove(validMoves):
    return random.choice(validMoves)
def findBestMove(gs, validMoves):
    global nextMove, counter
    counter = 0
    findMoveMinMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else 0)
    # findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)

    #findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    print(counter)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return scoreMaterial(gs.board)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def findMoveMinMaxAlphaBeta(gs, validMoves, depth, alpha, beta, whiteToMove):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return scoreBoard(gs)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMaxAlphaBeta(gs, nextMoves, depth - 1, alpha, beta, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
            if maxScore >= beta:
                break
            if maxScore > alpha:
                alpha = maxScore
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMaxAlphaBeta(gs, nextMoves, depth - 1, alpha, beta, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
            if minScore <= alpha:
                break
            if minScore < beta:
                beta = minScore
        return minScore


def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier*scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = - findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier*scoreBoard(gs)
    #move ordering - implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = - findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1,-beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: #pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore
"""
A positive score is good for white, a negative score is good for black
"""
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE #black win
        else:
            return CHECKMATE #white win
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                #score it positionally
                piecePositionScore = 0;
                if square[1] != 'K':
                    piecePositionScore = piecePositionScores[square][row][col]
                if square[0] == 'w':
                    score += (pieceScore[square[1]] + piecePositionScore)
                elif square[0] == 'b':
                    score -= (pieceScore[square[1]] + piecePositionScore)
    return score
"""
Score the board based on material
"""
def scoreMaterial(board):
    score = 0
    for row in  board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score