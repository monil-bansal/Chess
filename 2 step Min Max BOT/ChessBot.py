import random

# A map of piece to score value -> Standard chess scores
pieceScore = {'K': 0, "P": 1, "N": 3, "B": 3, "R": 5, "Q": 9}   #making King = 0, as no one can actually take the king
CHECKMATE = 1000    # if you lead to checkmate you win -> hence max attainable score
STALEMATE = 0       # If you can win(capture opponent's piece) avoid it but if you loosing(opponent can give you Checkmate) try it hence 0 and not -1000

'''
    Function to calculate RANDOM move from the list of valid moves.
'''
def findRandomMove(validMoves):
    if len(validMoves) > 0:
        return validMoves[random.randint(0, len(validMoves) - 1)]


'''
    Function to find the BEST move from the list of valid moves
'''
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1    # for allowing AI to play as any color
    playerMaxScore = -CHECKMATE    # as AI is playing Black this is the worst possible score -> AI will start from worst and try to improve
    bestMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:   # not assigning colors so AI can play as both: playerMove -> move of the current player || opponentMove -> opponent's move
        gs.makeMove(playerMove)
        opponentMinScore = CHECKMATE
        opponentMoves = gs.getValidMoves()
        if gs.checkMate:
            gs.undoMove()
            return playerMove
        elif gs.staleMate:
            opponentMinScore = STALEMATE
        else:
            for opponentMove in opponentMoves:
                gs.makeMove(opponentMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = -CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = turnMultiplier * boardScore(gs.board)
                if score < opponentMinScore:
                    opponentMinScore = score
                gs.checkMate = False
                gs.staleMate = False
                gs.undoMove()
        if playerMaxScore < opponentMinScore:
            playerMaxScore = opponentMinScore
            bestMove = playerMove
        gs.undoMove()
    return bestMove


'''
    Gives the score of the board according to the material on it -> White piece positive material and Black piece negative material.
    Assuming that Human is playing White and BOT is playing black
'''
def boardScore(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score


