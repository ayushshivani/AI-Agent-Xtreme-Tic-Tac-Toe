import sys
import random
import signal
import time
import copy
# from simulator import BigBoard

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
	
	def heuristic(self,board,flg):

		cross_score = 0
		oval_score = 0
		# print len(board.big_boards_status)
		for i in range(9):
			for k in range(2):
				for j in range(9):
					#center square of any board
					if i %3 == 1 and j%3==1:
						if board.big_boards_status[k][i][j] == 'x':
							cross_score += 3
						else :
							oval_score += 3
					elif (i %3 ==1 and j%3 != 1) or (i%3!=1 and j%3==1):
						pass
					else:
						if board.big_boards_status[k][i][j] == 'x':
							cross_score += 2
						else :
							oval_score += 2
					
					#center square of full board

					if i == 4 and j == 4:
						if board.big_boards_status[k][i][j] == 'x':
							cross_score += 3
						else : 
							oval_score += 3

		for i in range(3):
			for k in range(2):
				for j in range(3):

					if board.small_boards_status[k][i][j] == 'x':
						cross_score += 5
					else : 
						oval_score += 5
						


					if i==1 and j==1:
						if board.small_boards_status[k][i][j] == 'x':
							cross_score += 10
						else : 
							oval_score += 10 

					elif (i %3==1 and j %3 !=1) or (i%3!=1 and j%3==1):
						pass
					else:
						if board.small_boards_status[k][i][j] == 'x':
							cross_score += 3
						else :
							oval_score += 3

		# print cross_score,oval_score
		if(flg == 'o') :
			return oval_score
		else : 
			return cross_score     

	def minmax(self,cur_board,old_move,flg,dep):
		flg2 = 'o'
		if flg == 'o' : 
			flg2 = 'x'
		if dep == 2 :
			return self.heuristic(cur_board,flg) 
		elif dep == 1 :
			allowed_cells = self.find_valid_move_cells(cur_board,old_move)
			mn = inf
			mnx = 0
			mny = 0
			mnz = 0
			if allowed_cells is not None: 
				for i in range(len(allowed_cells)):
					x = allowed_cells[i][0]
					y = allowed_cells[i][1]
					z = allowed_cells[i][2]
					cur_board.big_boards_status[x][y][z]=flg 
					val = self.minmax(cur_board,flg2,(x,y,z),dep+1)
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
			if allowed_cells is not None: 
				for i in range(len(allowed_cells)):
					x = allowed_cells[i][0]
					y = allowed_cells[i][1]
					z = allowed_cells[i][2]
					cur_board.big_boards_status[x][y][z]=flg 
					val = self.minmax(cur_board,(x,y,z),flg2,dep+1)
					if val > mx:
						mx = val
						mxx = x 
						mxy = y
						mxz = z
					cur_board.big_boards_status[x][y][z]='-'
				return (x,y,z)



	def move(self,board,old_move,flg):
		cur_board = copy.copy(board)
		cur_move = self.minmax(cur_board,old_move,flg,0)
		x = cur_move[0]
		y = cur_move[1]
		z = cur_move[2]
		return (x,y,z)


# board = BigBoard()
# player = MyPlayer()
# player.heuristic(board)