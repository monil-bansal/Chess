"""
This is our main driver file. It will be responsible for 
	- handling user input
	- displaying current GameState object
"""
#Working with arguments to see which algorithm to use for the Chess Engine -> Basic, Advances;
import sys
import pygame as p
if len(sys.argv) > 1 and (sys.argv[1]).lower() == 'adv':
	import ChessEngineAd as ChessEngine
else:
	import ChessEngine
import ChessBot
p.init()

WIDTH = HEIGHT = 480
DIMENTION = 8	 # 8*8 CHESS BOARD
SQ_SIZE = HEIGHT // DIMENTION
MAX_FPS = 15
IMAGES = {}
 
'''
Initialise the global dictionary of images. This will be called exactly once in the main
'''
def loadImages():
	pieces = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wB', 'wQ', 'wK']
	for piece in pieces:
		IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
	# Note: We can access a piece by saying IMAGES['wP'] -> will give white pawn; 
 
'''
This will be out main driver. It will handle user input and update the graphics.
'''
def main():
	screen = p.display.set_mode((WIDTH, HEIGHT))
	clock = p.time.Clock()
	screen.fill(p.Color('white'))
	gs = ChessEngine.GameState()
	validMoves = gs.getValidMoves()		# get a list of valid moves.
	moveMade = False		 			# to check if the user made a move. If true recalculate validMoves.
	loadImages()						# only do this once -> before the while loop
	running = True
	animate = False		 				# Flag variable to note when we should animate the piece movement
	sqSelected = ()		 				# no sq is selected initially, keep track of the last click by the user -> (tuple : (row,col))
	playerClicks = []					# contains players clicks => [(6,4),(4,4)]  -> pawn at (6,4) moved 2 steps up on (4,4)
	playerOne = True					# if Human is playing white -> this will be true
	playerTwo = False					# if Human is playing black -> this will be true
	gameOver = False					# True in case of Checkmate and Stalemate
	while running:
		humanTurn = not (gs.whiteToMove ^ playerOne)
		for e in p.event.get():
			if e.type == p.QUIT:
				running = False
			#MOUSE HANDLERS
			elif e.type == p.MOUSEBUTTONDOWN:
				if not gameOver and humanTurn:
					location = p.mouse.get_pos()	 # (x,y) position of mouse
					col = location[0]//SQ_SIZE
					row = location[1]//SQ_SIZE
					if sqSelected == (row, col): 	# user selected the same sq. twice -> deselect the selecion
						sqSelected = ()
						playerClicks = []
					else:
						sqSelected = (row, col)
						playerClicks.append(sqSelected)	 # append for both 1st and 2nd click
						if len(playerClicks) == 2: 	# when 2nd click
							move = ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)
							for i in range(len(validMoves)):
								if move == validMoves[i]:
									gs.makeMove(validMoves[i])
									moveMade = True
									animate = True
									playerClicks = [] 	# reset playerClicks
									sqSelected = () 	# reset user clicks
							if not moveMade:
								playerClicks = [sqSelected]



			#KEY HANDLERS
			elif e.type == p.KEYDOWN:
				if e.key == p.K_z:		#undo last move id 'z' is pressed
					gs.undoMove()
					gameOver = False
					moveMade = True	 	# can do `validMoves = gs.validMoves()` but then if we change function name we will have to change the call at various places.
				if e.key == p.K_r: 	#reset the game if 'r' is pressed
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
			if AIMove is None:		# If AI can't find any move -> if any move will lead to opponent giving a checkmate.
				AIMove = ChessBot.findRandomMove(validMoves)
			gs.makeMove(AIMove)
			moveMade = True
			animate = True

		if moveMade:
			if len(gs.moveLog) > 0 and animate:
				animate = False
				animateMove(gs.moveLog[-1], screen, gs.board, clock)
			validMoves = gs.getValidMoves()
			moveMade = False

		drawGameState(screen, gs, sqSelected, validMoves)

		if gs.checkMate:
			gameOver = True
			if gs.whiteToMove:
				drawText(screen, "Black Won by Checkmate!");
			else:
				drawText(screen, "White Won by Checkmate!");

		if gs.staleMate:
			gameOver = True
			drawText(screen, "Draw due to Stalemate!")

		clock.tick(MAX_FPS) 
		p.display.flip()


'''
For highlighting the correct sq. of selected piece and the squares it can move to
'''
def highlightSquares(screen, gs, selectedSquare, validMoves):
	if selectedSquare != ():
		r, c = selectedSquare
		enemyColor = 'b' if gs.whiteToMove else 'w'
		allyColor = 'w' if gs.whiteToMove else 'b'
		if gs.board[r][c][0] == allyColor:
			#Highlighting the selected Square
			s = p.Surface((SQ_SIZE, SQ_SIZE))
			s.set_alpha(100)		# transparency value -> 0 : 100% transparent | 255 : 100% Opaque
			s.fill(p.Color('blue'))
			screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))

			#Highlighting the valid move squares
			s.fill(p.Color('yellow'))
			for move in validMoves:
				if move.startRow == r and move.startCol == c:
					endRow = move.endRow
					endCol = move.endCol
					if gs.board[endRow][endCol] == '--' or gs.board[endRow][endCol][0] == enemyColor:
						screen.blit(s, (endCol * SQ_SIZE, endRow * SQ_SIZE))


'''
responsible for all the graphics in the game
'''
def drawGameState(screen, gs, selectedSquare, validMoves):
	drawBoard(screen) 	#draw squares on board (should be called before drawing anything else)
	highlightSquares(screen, gs, selectedSquare, validMoves)
	drawPieces(screen, gs.board) 	#draw pieces on the board


'''
draw the squares on the board
'''
def drawBoard(screen):
	global colors
	colors = [p.Color(235, 235, 208), p.Color(119, 148, 85)]
	for r in range(DIMENTION):
		for c in range(DIMENTION):
			color = colors[(r+c)%2]
			p.draw.rect(screen, color, p.Rect(SQ_SIZE*c, SQ_SIZE*r , SQ_SIZE, SQ_SIZE))



'''
draw the pieces on the board using ChessEngine.GameState.board.
'''
def drawPieces(screen, board):
	for r in range(DIMENTION):
		for c in range(DIMENTION):
			piece = board[r][c]
			if piece != '--':
				screen.blit(IMAGES[piece], p.Rect(SQ_SIZE*c, SQ_SIZE*r , SQ_SIZE, SQ_SIZE))


'''
Animates the movement of piece
'''
def animateMove(move, screen, board, clock):
	global colors
	dR = move.endRow - move.startRow
	dC = move.endCol - move.startCol
	framesPerSquare = 3		# frames to move 1 square
	frameCount = (abs(dR) + abs(dC)) * framesPerSquare
	for frame in range(frameCount + 1):
		r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
		drawBoard(screen)
		drawPieces(screen, board)
		#erase piece from endRow, endCol
		color = colors[(move.endRow + move.endCol) % 2]
		endSqaure = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
		p.draw.rect(screen, color, endSqaure)
		#draw captured piece back
		# if move.pieceCaptured != '--':
			# screen.blit(IMAGES[move.pzieceCaptured], endSqaure)
		#draw moving piece
		screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
		p.display.flip()
		clock.tick(60)

'''
To wrtie some text in the middle of the screen!
'''
def drawText(screen, text):
						#  Font Name  Size Bold  Italics
	font = p.font.SysFont("Helvitica", 32, True, False);
	textObject = font.render(text, 0, p.Color('Blue'))
	textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
	screen.blit(textObject, textLocation)



if __name__ == '__main__':
	main()





























