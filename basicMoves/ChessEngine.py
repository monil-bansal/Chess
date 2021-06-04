"""
This is responsible for:
	- storing all the information about the current game state.
	- determining the valid moves 
	- will keep a move log (for doing undo  and look back into current game) 
"""

class GameState():
	def __init__(self):
		# board is a 8*8 2D list
		# each element is a 2 character long string consisting of 
			# - lower case (b/w) as color 
			# - upper case (R,N,B,Q,K or P) as piece name
		# in case the cell is empty then we store '--'
		self.board = [
			['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
			['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
	 		['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
		self.whiteToMove = True
		self.moveLog = []

	def makeMove(self, move):
		self.board[move.startRow][move.startCol] = '--'  # empty the start cell 
		self.board[move.endRow][move.endCol] = move.pieceMoved 	# keep the piece moved on the end cell
		self.moveLog.append(move) 	# record the move
		self.whiteToMove = not self.whiteToMove	 # swap the turn

class Move():

	#maps keys to values
	#For converting (row, col) to Chess Notations => (0,0) -> a8
	ranksToRows = {"1": 7 , "2": 6, "3": 5, "4": 4, 
				   "5": 3, "6": 2, "7": 1, "8": 0 }
	rowsToRanks = {v:k  for k,v in ranksToRows.items()}
	filesToCols = {"a":0, "b":1, "c":2, "d":3,
				   "e":4, "f":5, "g":6, "h":7}
	colsToFiles = {v:k  for k,v in filesToCols.items()}

	def __init__(self, startSq, endSq, board):
		self.startRow = startSq[0]
		self.startCol = startSq[1]
		self.endRow = endSq[0]
		self.endCol = endSq[1]
		self.pieceMoved = board[self. startRow][self. startCol] # can't be '--' 
		self.pieceCaptured = board[self. endRow][self. endCol]  # can be '--' -> no piece was captured 

	def getChessNotation(self):
		return self.getFileRank(self.startRow,self.startCol) + self.getFileRank(self.endRow,self.endCol) 

	def getFileRank (self, r, c):
		return self.colsToFiles[c] + self.rowsToRanks[r]


