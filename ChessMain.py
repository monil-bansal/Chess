"""
This is our main driver file. It will be responsible for 
	- handling user input
	- displaying current GameState object
"""
# Working with arguments to see which algorithm to use for the Chess Engine -> Basic, Advances;
import sys
import pygame as p

if len(sys.argv) > 1 and (sys.argv[1]).lower() == 'adv':
    import ChessEngineAd as ChessEngine
else:
    import ChessEngine
import ChessBot
import config

p.init()

BOARD_WIDTH = BOARD_HEIGHT = config.BOARD_WIDTH
MOVE_LOG_PANNEL_WIDTH = config.MOVE_LOG_PANNEL_WIDTH
MOVE_LOG_PANNEL_HEIGHT = config.MOVE_LOG_PANNEL_HEIGHT
DIMENTION = config.DIMENTION  # 8*8 CHESS BOARD
SQ_SIZE = BOARD_HEIGHT // DIMENTION
MAX_FPS = config.MAX_FPS
IMAGES = {}
MOVE_LOG_FONT = p.font.SysFont(config.MOVE_LOG_FONT_NAME, config.MOVE_LOG_FONT_SIZE, False, False)

'''
Initialise the global dictionary of images. This will be called exactly once in the main
'''


def loadImages():
    pieces = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(config.IMAGE_FOLDER + piece + ".png"), (SQ_SIZE, SQ_SIZE))


# Note: We can access a piece by saying IMAGES['wP'] -> will give white pawn;

'''
This will be out main driver. It will handle user input and update the graphics.
'''


def main():
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANNEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()  # get a list of valid moves.
    moveMade = False  # to check if the user made a move. If true recalculate validMoves.
    loadImages()  # only do this once -> before the while loop
    running = True
    animate = False  # Flag variable to note when we should animate the piece movement
    sqSelected = ()  # no sq is selected initially, keep track of the last click by the user -> (tuple : (row,col))
    playerClicks = []  # contains players clicks => [(6,4),(4,4)]  -> pawn at (6,4) moved 2 steps up on (4,4)
    playerOne = config.PLAYER_ONE_HUMAN  # if Human is playing white -> this will be true
    playerTwo = config.PLAYER_TWO_HUMAN  # if Human is playing black -> this will be true
    gameOver = False  # True in case of Checkmate and Stalemate
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # MOUSE HANDLERS
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()  # (x,y) position of mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if not playerOne:
                        row, col = blackPerspectiveRow(row, col)
                    if (col >= 8) or col < 0:  # Click out of board (on move log panel) -> do nothing
                        continue
                    if sqSelected == (row, col):  # user selected the same sq. twice -> deselect the selecion
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # append for both 1st and 2nd click
                        if len(playerClicks) == 2:  # when 2nd click
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    playerClicks = []  # reset playerClicks
                                    sqSelected = ()  # reset user clicks
                            if not moveMade:
                                playerClicks = [sqSelected]



            # KEY HANDLERS
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo last move id 'z' is pressed
                    gs.undoMove()
                    gameOver = False
                    moveMade = True  # can do `validMoves = gs.validMoves()` but then if we change function name we will have to change the call at various places.
                if e.key == p.K_r:  # reset the game if 'r' is pressed
                    gs = ChessEngine.GameState()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    validMoves = gs.getValidMoves()

        # AI Move finder logic
        if not gameOver and not humanTurn:
            AIMove = ChessBot.findBestMoveMinMax(gs, validMoves)
            if AIMove is None:  # If AI can't find any move -> if any move will lead to opponent giving a checkmate.
                AIMove = ChessBot.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if len(gs.moveLog) > 0 and animate:
                animate = False
                animateMove(gs.moveLog[-1], screen, gs.board, clock, playerOne)
            validMoves = gs.getValidMoves()

            moveMade = False

        drawGameState(screen, gs, sqSelected, validMoves, playerOne)

        # Print Checkmate
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen, "Black Won by Checkmate!");
            else:
                drawEndGameText(screen, "White Won by Checkmate!");

        # Print Stalmate
        if gs.staleMate:
            gameOver = True
            drawEndGameText(screen, "Draw due to Stalemate!")

        clock.tick(MAX_FPS)
        p.display.flip()


'''
Calculate Row for Black's perspective
'''


def blackPerspectiveRow(r, c):
    return (7 - r, 7 - c)


'''
responsible for all the graphics in the game
'''


def drawGameState(screen, gs, selectedSquare, validMoves, whitesPerspective):
    drawBoard(screen)  # draw squares on board (should be called before drawing anything else)
    highlightSquares(screen, gs, selectedSquare, validMoves, whitesPerspective)
    highlightCheck(screen, gs, whitesPerspective)
    if len(gs.moveLog) > 0:
        highlightLastMove(screen, gs.moveLog[-1], whitesPerspective)
    drawPieces(screen, gs.board, whitesPerspective)  # draw pieces on the board
    drawMoveLog(screen, gs)


'''
draw the squares on the board
'''


def drawBoard(screen):
    global colors
    colors = [config.BOARD_COLOR_LIGHT, config.BOARD_COLOR_DARK]
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(SQ_SIZE * c, SQ_SIZE * r, SQ_SIZE, SQ_SIZE))


'''
Highlight Check
'''


def highlightCheck(screen, gs, whitesPerspective):
    if gs.inCheck:
        r, c = gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation
        if not whitesPerspective:
            r, c = blackPerspectiveRow(r, c)
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)  # transparency value -> 0 : 100% transparent | 255 : 100% Opaque
        s.fill(p.Color('red'))
        screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


'''
For highlighting the correct sq. of selected piece and the squares it can move to
'''


def highlightSquares(screen, gs, selectedSquare, validMoves, whitesPerspective):
    if selectedSquare != ():
        r, c = selectedSquare
        r1, c1 = r, c
        if not whitesPerspective:
            r1, c1 = blackPerspectiveRow(r, c)
        enemyColor = 'b' if gs.whiteToMove else 'w'
        allyColor = 'w' if gs.whiteToMove else 'b'
        if gs.board[r][c][0] == allyColor:
            # Highlighting the selected Square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value -> 0 : 100% transparent | 255 : 100% Opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c1 * SQ_SIZE, r1 * SQ_SIZE))

            # Highlighting the valid move squares
            s.fill(p.Color('yellow'))

            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    endRow = move.endRow
                    endCol = move.endCol
                    drawEndRow, drawEndCol = endRow, endCol
                    if not whitesPerspective:
                        drawEndRow, drawEndCol = blackPerspectiveRow(endRow, endCol)
                    if gs.board[endRow][endCol] == '--' or gs.board[endRow][endCol][0] == enemyColor:
                        screen.blit(s, (drawEndCol * SQ_SIZE, drawEndRow * SQ_SIZE))


'''
Highlight the last move
'''


def highlightLastMove(screen, move, whitesPerspective):
    startRow = move.startRow
    startCol = move.startCol
    endRow = move.endRow
    endCol = move.endCol
    if not whitesPerspective:
        startRow, startCol = blackPerspectiveRow(startRow, startCol)
        endRow, endCol = blackPerspectiveRow(endRow, endCol)
    s = p.Surface((SQ_SIZE, SQ_SIZE))
    s.set_alpha(100)
    s.fill(p.Color("pink"))
    screen.blit(s, (startCol * SQ_SIZE, startRow * SQ_SIZE))
    screen.blit(s, (endCol * SQ_SIZE, endRow * SQ_SIZE))


'''
	Draw the pieces on the board using ChessEngine.GameState.board.
'''


def drawPieces(screen, board, whitesPerspective):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            r1, c1 = r, c
            if not whitesPerspective:
                r1, c1 = blackPerspectiveRow(r, c)
            piece = board[r1][c1]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(SQ_SIZE * c, SQ_SIZE * r, SQ_SIZE, SQ_SIZE))


'''
	Draw the 12. Move Log
'''


def drawMoveLog(screen, gs):
    font = MOVE_LOG_FONT
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANNEL_WIDTH, MOVE_LOG_PANNEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), moveLogRect)
    moveLog = []
    for i in range(0, len(gs.moveLog), 2):
        moveText = str(i // 2 + 1) + ".  " + gs.moveLog[i].getChessNotation()
        if i < len(gs.moveLog) - 1:
            moveText += "   " + gs.moveLog[i + 1].getChessNotation()
        moveLog.append(moveText)

    horizontalPadding = 5
    verticalPadding = 5
    lineSpacing = 5
    for i in range(len(moveLog)):
        textObject = font.render(moveLog[i], True, p.Color('white'))
        if (verticalPadding + textObject.get_height() >= (MOVE_LOG_PANNEL_HEIGHT - 1)):
            # if i > 1
            verticalPadding = 5
            horizontalPadding += 100
        textLocation = p.Rect(moveLogRect.move(horizontalPadding, verticalPadding))
        verticalPadding += textObject.get_height() + lineSpacing

        screen.blit(textObject, textLocation)
    if gs.checkMate:
        textObject = font.render("#", True, p.Color('Red'))
        textLocation = p.Rect(moveLogRect.move(horizontalPadding, verticalPadding))
        screen.blit(textObject, textLocation)
    if gs.staleMate:
        textObject = font.render("!", True, p.Color('Blue'))
        textLocation = p.Rect(moveLogRect.move(horizontalPadding, verticalPadding))
        screen.blit(textObject, textLocation)


'''
Animates the movement of piece
'''


def animateMove(move, screen, board, clock, whitesPerspective):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 3  # frames to move 1 square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    drawEndRow, drawEndCol = move.endRow, move.endCol
    drawStartRow, drawStartCol = move.startRow, move.startCol
    if not whitesPerspective:
        drawStartRow, drawStartCol = blackPerspectiveRow(move.startRow, move.startCol)
        drawEndRow, drawEndCol = blackPerspectiveRow(move.endRow, move.endCol)
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        if not whitesPerspective:
            r, c = blackPerspectiveRow(r, c)
        drawBoard(screen)
        drawPieces(screen, board, whitesPerspective)
        # erase piece from endRow, endCol
        color = colors[(drawEndRow + drawEndCol) % 2]
        endSqaure = p.Rect(drawEndCol * SQ_SIZE, drawEndRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSqaure)
        # draw captured piece back
        if move.pieceCaptured != '--':
            if move.enPassant:
                endSqaure = p.Rect(drawEndCol * SQ_SIZE, drawStartRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSqaure)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


'''
To wrtie some text in the middle of the screen!
'''


def drawEndGameText(screen, text):
    #  Font Name  Size Bold  Italics
    font = p.font.SysFont('Helvitica', 32, True, False)
    textObject = font.render(text, 0, p.Color('White'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))
    textObject = font.render(text, 0, p.Color('Blue'))
    screen.blit(textObject, textLocation.move(4, 4))


if __name__ == '__main__':
    main()
