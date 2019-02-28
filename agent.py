import sys
import random
import signal
import time
import copy
inf = 10000000000
class MyPlayer():

	def __init__(self):
		pass

	def find_valid_move_cells(self, board,old_move):
	#returns the valid cells allowed given the last move and the current board state
		# print("in find")
		# print(old_move)
		allowed_cells = []
		allowed_small_board = [old_move[1]%3, old_move[2]%3]
	#checks if the move is a free move or not based on the rules

		if old_move == (-1,-1,-1) or (board.small_boards_status[0][allowed_small_board[0]][allowed_small_board[1]] != '-' and board.small_boards_status[1][allowed_small_board[0]][allowed_small_board[1]] != '-'):
			for k in range(2):
				for i in range(9):
					for j in range(9):
						if board.big_boards_status[k][i][j] == '-' and board.small_boards_status[k][i/3][j/3] == '-':
							allowed_cells.append((k,i,j))

		else:
			for k in range(2):
				if board.small_boards_status[k][allowed_small_board[0]][allowed_small_board[1]] == "-":
					for i in range(3*allowed_small_board[0], 3*allowed_small_board[0]+3):
						for j in range(3*allowed_small_board[1], 3*allowed_small_board[1]+3):
							if board.big_boards_status[k][i][j] == '-':
								allowed_cells.append((k,i,j))

		return allowed_cells
	
	def heuristic(self,board):
		return 1

	def minmax(self,cur_board,old_move,dep):
		print(2)
		if dep == 2 :
			return self.heuristic(cur_board) 
		elif dep == 1 :
			allowed_cells = self.find_valid_move_cells(cur_board,old_move)
			mn = inf
			mnx = 0
			mny = 0
			mnz = 0
			print allowed_cells
			if allowed_cells is not None: 
				for i in range(len(allowed_cells)):
					x = allowed_cells[i][0]
					y = allowed_cells[i][1]
					z = allowed_cells[i][2]
					cur_board.big_boards_status[x][y][z]='O' 
					val = self.minmax(cur_board,(x,y,z),dep+1)
					if val < mn:
						mn = val
						mnx = x 
						mny = y
						mnz = z
					cur_board.big_boards_status[x][y][z]='-'
				return (x,y,z)
		else :
			allowed_cells = self.find_valid_move_cells(cur_board,old_move)
			mx = 0
			mxx = 0
			mxy = 0
			mxz = 0
			print allowed_cells
			if allowed_cells is not None: 
				for i in range(len(allowed_cells)):
					x = allowed_cells[i][0]
					y = allowed_cells[i][1]
					z = allowed_cells[i][2]
					cur_board.big_boards_status[x][y][z]='O' 
					val = self.minmax(cur_board,(x,y,z),dep+1)
					if val > mx:
						mx = val
						mxx = x 
						mxy = y
						mxz = z
					cur_board.big_boards_status[x][y][z]='-'
				return (x,y,z)



	def move(self,board,old_move,flg):
		cur_board = copy.copy(board)
		cur_move = self.minmax(cur_board,old_move,0)
		x = cur_move[0]
		y = cur_move[1]
		z = cur_move[2]
		print(x,y,z)
		return (x,y,z)
