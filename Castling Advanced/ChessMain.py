"""
This is our main driver file. It will be responsible for 
	- handling user input
	- displaying current GameState object
"""
#Working with arguments to see which algorithm to use for the Chess Engine -> Baisc, Advances;
import sys
import pygame as p
if len(sys.argv) > 1 and (sys.argv[1]).lower() == 'adv':
	import ChessEngineAd as ChessEngine
else:
	import ChessEngine

p.init()

WIDTH = HEIGHT = 480
DIMENTION = 8 # 8*8 CHESS BOARD
SQ_SIZE = HEIGHT // DIMENTION
MAX_FPS = 15
IMAGES = {}
 
'''
Initialise the global dictionary of images. This will be called exactly once in the main
'''
def loadImages():
	pieces = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wB', 'wQ', 'wK']
	for piece in pieces:
		IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE ) )  
	# Note: We can access a piece by saying IMAGES['wP'] -> will give white pawn; 
 
'''
This will be out main driver. It will handle user input and update the graphics.
'''
def main():
	screen = p.display.set_mode((WIDTH, HEIGHT))
	clock = p.time.Clock()
	screen.fill(p.Color('white'))
	gs = ChessEngine.GameState()
	validMoves = gs.getValidMoves()  # get a list of valid moves. 
	moveMade = False # to check if the user made a move. If true recalculate validMoves.
	loadImages() #only do this once -> before the while loop
	running = True
	sqSelected = () #no sq is selected initially, keep track of the last click by the user -> (tuple : (row,col)) 
	playerClicks = [] # contains players clicks => [(6,4),(4,4)]  -> pawn at (6,4) moved 2 steps up on (4,4)
	while running:
		for e in p.event.get():
			if e.type == p.QUIT :
				runnin = False
			#MOUSE HANDLERS
			elif e.type == p.MOUSEBUTTONDOWN:
				location = p.mouse.get_pos() # (x,y) position of mouse 
				col = location[0]//SQ_SIZE
				row = location[1]//SQ_SIZE
				if sqSelected == (row, col): # user selected the same sq. twice -> deselect the selecion
					sqSelected = ()
					playerClicks = []
				else:
					sqSelected = (row,col)
					playerClicks.append(sqSelected) # append for both 1st and 2nd click
					if len(playerClicks) == 2: # when 2nd click
						move = ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)
						for i in range(len(validMoves)):
							if move == validMoves[i]:
								gs.makeMove(validMoves[i])
								moveMade = True
								playerClicks = [] # reset platerClicks
								sqSelected = () # reset user clicks
						if not moveMade :
							playerClicks = [sqSelected]

			#KEY HANDLERS
			elif e.type == p.KEYDOWN:
				if e.key == p.K_z:
					gs.undoMove() 
					moveMade = True #can do `validMoves = gs.validMoves()` but then if we change function name we will have to change the call at various places. 

		if moveMade:
			validMoves = gs.getValidMoves()
			moveMade = False
		drawGameState(screen, gs)
		clock.tick(MAX_FPS) 
		p.display.flip()  

'''
responsible for all the graphics in the game
'''
def drawGameState(screen, gs):
	drawBoard(screen) #draw squares on board (should be called before drawing anything else)
	drawPieces(screen, gs.board) #draw pieces on the board
	# FUTURE SCOPE : add in piece highlighting or move suggestions 


'''
draw the squares on the board
'''
def drawBoard(screen):
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



if __name__ == '__main__':
	main()





























