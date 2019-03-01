import sys
import random
import signal
import time
import copy
# from simulator import BigBoard

inf = 10000000000
class MyPlayer():
	
	def __init__(self):
		self.empty_small_board = "----------"
		self.small_board_score = {}
		self.empty_small_board = self.change(self.empty_small_board,9,'o') 
		self.preprocess(self.empty_small_board)
		self.empty_small_board = self.change(self.empty_small_board,9,'x') 
		self.preprocess(self.empty_small_board)

	def change(self,s,i,c):
		s = s[:i] + c + s[i+1:]
		return s

	def preprocess(self,bs):
		#checking for vertical pattern
		for i in range(3):
			if (bs[i] == bs[3+i] == bs[6+i]) and (bs[i] == 'o'):
				self.small_board_score[bs]=50
				return 50
			if (bs[i] == bs[3+i] == bs[6+i]) and (bs[i] == 'x'):
				self.small_board_score[bs]=-50
				return -50
			#checking for horizontal pattern
			if (bs[3*i] == bs[3*i+1] == bs[3*i+2]) and (bs[3*i+2] == 'o'):
				self.small_board_score[bs]=50
				return 50
			if (bs[3*i] == bs[3*i+1] == bs[3*i+2]) and (bs[3*i+2] == 'x'):
				self.small_board_score[bs]=-50
				return -50
		#checking for diagonal patterns
		#diagonal 1
		if (bs[0] == bs[4] == bs[8]) and (bs[0] == 'o'):
			self.small_board_score[bs]=50
			return 50
		if (bs[0] == bs[4] == bs[8]) and (bs[0] == 'x'):
			self.small_board_score[bs]=-50
			return -50
		#diagonal 2
		if (bs[2] == bs[4] == bs[6]) and (bs[2] == 'o'):
			self.small_board_score[bs]=50
			return 50
		if (bs[2] == bs[4] == bs[6]) and (bs[2] == 'x'):
			self.small_board_score[bs]=-50
			return -50
		if bs in self.small_board_score:
			return self.small_board_score[bs]
		#check if board is already complete
		flag = 0
		for i in range(9):
				if bs[i] != '-' :
					flag = flag + 1
		if flag == 9 :
			return 0
		ply = bs[9]
		if ply == 'o' :
			mx = -50
			for i in range(9):
				if bs[i] == '-':
					bs = self.change(bs,i,'o')
					bs = self.change(bs,9,'x')
					mx = max(mx,self.preprocess(bs))
					bs = self.change(bs,9,'o')
					self.preprocess(bs)
					bs = self.change(bs,i,'x')
					bs = self.change(bs,9,'x')
					self.preprocess(bs)
					bs = self.change(bs,9,'o')
					self.preprocess(bs)
					bs = self.change(bs,i,'-')
			self.small_board_score[bs] = mx
			# print(bs,mx)
			return mx
		else :
			mn = 50
			for i in range(9):
				if bs[i] == '-':
					bs = self.change(bs,i,'x')
					bs = self.change(bs,9,'o')
					mn = min(mn,self.preprocess(bs))
					bs = self.change(bs,9,'x')
					self.preprocess(bs)
					bs = self.change(bs,i,'o')
					bs = self.change(bs,9,'o')
					self.preprocess(bs)
					bs = self.change(bs,9,'x')
					self.preprocess(bs)
					bs = self.change(bs,i,'-')
			# print(bs,mn)
			self.small_board_score[bs] = mn
			return mn

	def find_valid_move_cells(self, board,old_move):
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
	
	def heuristic(self,board,flg):

		cross_score = 0
		oval_score = 0
		for i in range(3):
			for k in range(2):	
				for j in range(3):
					#centre
					if i==1 and j==1:
						if board.small_boards_status[k][i][j] == 'x':
							cross_score += 5
						if board.small_boards_status[k][i][j] == 'o':
							oval_score += 5 

					#middle
					elif (i %3==1 and j %3 !=1) or (i%3!=1 and j%3==1):
						if board.small_boards_status[k][i][j] == 'x':
							cross_score += 3
						if board.small_boards_status[k][i][j] == 'o':
							oval_score += 3 
					#corner
					else:
						if board.small_boards_status[k][i][j] == 'x':
							cross_score += 4
						if board.small_boards_status[k][i][j] == 'o':
							oval_score += 4

		# print cross_score,oval_score
		if(flg == 'o'):
			return oval_score - cross_score
		else : 
			return cross_score - oval_score

	def minmax(self,cur_board,old_move,flg,dep):
		flg2 = 'o'
		if flg == 'o' : 
			flg2 = 'x'
		if dep == 2 :
			return self.heuristic(cur_board,flg) 
		elif dep % 2 == 1 :
			allowed_cells = self.find_valid_move_cells(cur_board,old_move)
			mn = -inf
			mnx = 0
			mny = 0
			mnz = 0
			if allowed_cells is not None: 
				for i in range(len(allowed_cells)):
					x = allowed_cells[i][0]
					y = allowed_cells[i][1]
					z = allowed_cells[i][2]
					cur_board.big_boards_status[x][y][z]=flg 
					temp_board = ([['-' for i in range(3)] for j in range(3)])
					sty = y/3
					stz = z/3
					temp_board = ""

					for i in range(3):
						for j in range(3):
							temp_board += cur_board.big_boards_status[x][3*sty+i][3*stz+j]
					temp_board=self.change(temp_board,9,flg2)
					
					score = self.small_board_score[temp_board]
					
					if(flg=='x'):
						score =  -score						
					if score == 50 :
						cur_board.small_boards_status[x][sty][stz] = flg
					elif score == -50:
						cur_board.small_boards_status[x][sty][stz] = flg2
					else :
						cur_board.small_boards_status[x][sty][stz] = 'd'
					
					val = self.minmax(cur_board,(x,y,z),flg2,dep+1)
					if val < mn:
						mn = val
						mnx = x 
						mny = y
						mnz = z
					cur_board.big_boards_status[x][y][z]='-'
					cur_board.small_boards_status[x][sty][stz] = '-'					
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
					temp_board = ([['-' for i in range(3)] for j in range(3)])
					sty = y/3
					stz = z/3
					temp_board = ""

					for i in range(3):
						for j in range(3):
							temp_board += cur_board.big_boards_status[x][3*sty+i][3*stz+j]
					temp_board=self.change(temp_board,9,flg2)
					
					score = self.small_board_score[temp_board]
					
					if(flg=='x'):
						score =  -score						
					if score == 50 :
						cur_board.small_boards_status[x][sty][stz] = flg
					elif score == -50:
						cur_board.small_boards_status[x][sty][stz] = flg2
					else :
						cur_board.small_boards_status[x][sty][stz] = 'd'
					
					val = self.minmax(cur_board,(x,y,z),flg2,dep+1)
					if val > mx:
						mx = val
						mxx = x 
						mxy = y
						mxz = z
					cur_board.big_boards_status[x][y][z]='-'
					cur_board.small_boards_status[x][sty][stz] = '-'					
				return (x,y,z)



	def move(self,board,old_move,flg):
		cur_board = copy.deepcopy(board)
		cur_move = self.minmax(cur_board,old_move,flg,0)
		x = cur_move[0]
		y = cur_move[1]
		z = cur_move[2]
		return (x,y,z)


# board = BigBoard()
player = MyPlayer()
# player.heuristic(board)