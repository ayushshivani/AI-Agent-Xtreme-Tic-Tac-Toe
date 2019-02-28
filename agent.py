import sys
import random
import signal
import time
import copy
inf = 10000000000
class MyPlayer():

    def __init__(self):
    	pass

	def print_board(self):
		# for printing the state of the board
		print '================BigBoard State================'
		for i in range(9):
			if i%3 == 0:
				print
			for k in range(2):
				for j in range(9):
					if j%3 == 0:
						print "",
					print self.big_boards_status[k][i][j],
				if k==0:
					print "   ",
			print
		print

		print '==============SmallBoards States=============='
		for i in range(3):
			for k in range(2):
				for j in range(3):
					print self.small_boards_status[k][i][j],
				if k==0:
					print "  ",
			print
		print '=============================================='
		print
		print

 	def find_valid_move_cells(self,board,old_move):
		#returns the valid cells allowed given the last move and the current board state
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



	def check_valid_move(self, old_move, new_move):
		#checks if a move is valid or not given the last move
		if (len(old_move) != 3) or (len(new_move) != 3):
			return False
		for i in range(3):
			if (type(old_move[i]) is not int) or (type(new_move[i]) is not int):
				return False
		if (old_move != (-1,-1,-1)) and (old_move[0] < 0 or old_move[0] > 1 or old_move[1] < 0 or old_move[1] > 8 or old_move[2] < 0 or old_move[2] > 8):
			return False
		cells = self.find_valid_move_cells(old_move)
		return new_move in cells


	def minmax(self,cur_board,old_move,dep):
		print(2)
		if dep == 2 :
			return self.heuristic(cur_board) 
		elif dep == 1 :
			allowed_cells = self.find_valid_move_cells()
			mn = inf
			mn = min(mn,self.minmax(cur_board,(1,1,1),dep+1))
			return min
		else :
			allowed_cells = self.find_valid_move_cells()
			mx = 0
			mxx = 0
			mxy = 0
			mxz = 0
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


    def heuristic(self):
		print "Chut"
		return 

    def move(self,board,old_move,flg):
    	x = 1
    	print(1)
    	print(old_move)
    	cur_board = copy.copy(board)
    	self.heuristic()
    	# self.minmax(cur_board,old_move,0)
    	# x = cur_move[0]
    	# y = cur_move[1]
    	# z = cur_move[2]
    	# return (x,y,z)
