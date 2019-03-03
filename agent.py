import sys
import random
import signal
import time
import copy
# from simulator import BigBoard
gdep = 4
inf = 10000000000
class MyPlayer():
	
	def __init__(self):
		self.empty_small_board = "----------"
		self.small_board_score = {}
		self.empty_small_board = self.change(self.empty_small_board,9,'o') 
		# self.preprocess(self.empty_small_board)
		self.empty_small_board = self.change(self.empty_small_board,9,'x') 
		# self.preprocess(self.empty_small_board)

	def change(self,s,i,c):
		s = s[:i] + c + s[i+1:]
		return s
	def check_small_board_won(self,bs):
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
		return 0
	def preprocess(self,bs):
	
		x = self.check_small_board_won(bs)
		if  x == 50 or x == -50:
 			self.small_board_score[bs]=x
			return x

		#check if board is already complete
		flag = 0
		for i in range(9):
				if bs[i] != '-' :
					flag = flag + 1
		if flag == 9 :
			self.small_board_score[bs]= 0
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


	def checking_win(self,bs,flg):
		score = 0
		no_x = 0 
		no_o = 0
		oval_score = 0
		cross_score = 0 
		for k in range(2):
			for i in range(3):
						#checking for horizontal pattern(i'th row)
				if (bs[k][i][0] == bs[k][i][1] == bs[k][i][2]) and (bs[k][i][0] == 'o'):
					oval_score = 10000
				if (bs[k][i][0] == bs[k][i][1] == bs[k][i][2]) and (bs[k][i][0] == 'x'):
					cross_score = 10000
				#checking for vertical pattern(i'th column)
				if (bs[k][0][i] == bs[k][1][i] == bs[k][2][i]) and (bs[k][0][i] == 'o'):
					oval_score = 10000
				if (bs[k][0][i] == bs[k][1][i] == bs[k][2][i]) and (bs[k][0][i] == 'x'):
					cross_score = 10000	
			#checking for diagonal patterns
			#diagonal 1
			x= 0 
			y =0
			if (bs[k][3*x][3*y] == bs[k][3*x+1][3*y+1] == bs[k][3*x+2][3*y+2]) and (bs[k][3*x][3*y] == 'o'):
				oval_score = 10000
			if (bs[k][3*x][3*y] == bs[k][3*x+1][3*y+1] == bs[k][3*x+2][3*y+2]) and (bs[k][3*x][3*y] == 'x'):
				cross_score = 10000
			
			#diagonal 2
			if (bs[k][3*x][3*y+2] == bs[k][3*x+1][3*y+1] == bs[k][3*x+2][3*y]) and (bs[k][3*x][3*y+2] == 'o'):
				oval_score = 10000
			if (bs[k][3*x][3*y+2] == bs[k][3*x+1][3*y+1] == bs[k][3*x+2][3*y]) and (bs[k][3*x][3*y+2] == 'x'):
				cross_score = 10000

		
		for k in range(2):
			for i in range(3):
				for j in range(3):
					if bs[k][i][j] == 'x':
						no_x += 1
					elif bs[k][i][j] == 'o':
						no_o += 1
		oval_score += 100 *no_o
		cross_score += 100*no_x

		return (oval_score,cross_score)
<<<<<<< HEAD
=======
	
	def check_small_board_score(self,bs):
		# middle zero and corner  
		if bs[1][1] == 'x':
			if bs[0][0] == 'x' or bs[0][2] == 'x' or bs[2][0] == 'x' or bs[2][2] == 'x':
				cross_score += a4

		if bs[1][1] == 'o':
			if bs[0][0] == 'o' or bs[0][2] == 'o' or bs[2][0] == 'o' or bs[2][2] == 'o':
				oval_score += a4


		# middle and corner d
		if bs[1][1] == 'x':
			if bs[0][1] == 'x' or bs[1][0] == 'x' or bs[1][2] == 'x' or bs[2][1] == 'x':
				cross_score += a2


		if bs[1][1] == 'o':
			if bs[0][1] == 'o' or bs[1][0] == 'o' or bs[1][2] == 'o' or bs[2][1] == 'o':
				oval_score  += a2

		#corner and middle middle
		if bs[0][1] == 'x':
			if bs[0][0] == 'x' or bs[0][2] == 'x':
				cross_score += a1

		if bs[2][1] == 'x':
			if bs[2][0] == 'x' or bs[2][2] == 'x':
				cross_score += a1

		if bs[0][1] == 'o':
			if bs[0][0] == 'o' or bs[0][2] == 'o':
				oval_score += a1

		if bs[2][1] == 'o':
			if bs[2][0] == 'o' or bs[2][2] == 'o':
				oval_score += a1

		#vertical

		if bs[1][0] == 'x':
			if bs[0][0] == 'x' or bs[2][0] == 'x':
				cross_score += a1

		if bs[1][2] == 'x':
			if bs[0][2] == 'x' or bs[2][2] == 'x':
				cross_score += a1

		if bs[1][0] == 'o':
			if bs[0][0] == 'o' or bs[2][0] == 'o':
				oval_score += a1

		if bs[1][2] == 'o':
			if bs[0][2] == 'o' or bs[2][2] == 'o':
				oval_score += a1
		return (oval_score,cross_score)
>>>>>>> 05f4f367f2c3d9240c143ad76ba2104663038e99


	def heuristic(self,board,flg):

		cross_score = 0
		oval_score = 0
		# print(board)
		a4 = 400
		a3 = 300
		a2 = 200
		a1 = 100

		for k in range(2):
			# middle zero and corner  
			if board.small_boards_status[k][1][1] == 'x':
				if board.small_boards_status[k][0][0] == 'x' or board.small_boards_status[k][0][2] == 'x' or board.small_boards_status[k][2][0] == 'x' or board.small_boards_status[k][2][2] == 'x':
					cross_score += a4

			if board.small_boards_status[k][1][1] == 'o':
				if board.small_boards_status[k][0][0] == 'o' or board.small_boards_status[k][0][2] == 'o' or board.small_boards_status[k][2][0] == 'o' or board.small_boards_status[k][2][2] == 'o':
					oval_score += a4


			# middle and corner d
			if board.small_boards_status[k][1][1] == 'x':
				if board.small_boards_status[k][0][1] == 'x' or board.small_boards_status[k][1][0] == 'x' or board.small_boards_status[k][1][2] == 'x' or board.small_boards_status[k][2][1] == 'x':
					cross_score += a2


			if board.small_boards_status[k][1][1] == 'o':
				if board.small_boards_status[k][0][1] == 'o' or board.small_boards_status[k][1][0] == 'o' or board.small_boards_status[k][1][2] == 'o' or board.small_boards_status[k][2][1] == 'o':
					oval_score += a2

			#corner and middle middle
			if board.small_boards_status[k][0][1] == 'x':
				if board.small_boards_status[k][0][0] == 'x' or board.small_boards_status[k][0][2] == 'x':cross_score += a1

			if board.small_boards_status[k][2][1] == 'x':
				if board.small_boards_status[k][2][0] == 'x' or board.small_boards_status[k][2][2] == 'x':cross_score += a1

			if board.small_boards_status[k][0][1] == 'o':
				if board.small_boards_status[k][0][0] == 'o' or board.small_boards_status[k][0][2] == 'o':
					oval_score += a1

			if board.small_boards_status[k][2][1] == 'o':
				if board.small_boards_status[k][2][0] == 'o' or board.small_boards_status[k][2][2] == 'o':oval_score += a1

			#vertical

			if board.small_boards_status[k][1][0] == 'x':
				if board.small_boards_status[k][0][0] == 'x' or board.small_boards_status[k][2][0] == 'x':cross_score += a1

			if board.small_boards_status[k][1][2] == 'x':
				if board.small_boards_status[k][0][2] == 'x' or board.small_boards_status[k][2][2] == 'x':cross_score += a1

			if board.small_boards_status[k][1][0] == 'o':
				if board.small_boards_status[k][0][0] == 'o' or board.small_boards_status[k][2][0] == 'o':
					oval_score += a1

			if board.small_boards_status[k][1][2] == 'o':
				if board.small_boards_status[k][0][2] == 'o' or board.small_boards_status[k][2][2] == 'o':oval_score += a1





		for i in range(3):
			for k in range(2):
				for j in range(3):
					#centre
					if i==1 and j==1:
						if board.small_boards_status[k][i][j] == 'x':
							cross_score += 10
						if board.small_boards_status[k][i][j] == 'o':
							oval_score += 10

					#middle
					elif (i %3==1 and j %3 !=1) or (i%3!=1 and j%3==1):
						if board.small_boards_status[k][i][j] == 'x':
							cross_score += 3
						if board.small_boards_status[k][i][j] == 'o':
							oval_score += 3 
					#corner
					else:
						if board.small_boards_status[k][i][j] == 'x':
							cross_score += 6
						if board.small_boards_status[k][i][j] == 'o':
							oval_score += 6

		
		score = self.checking_win(board.small_boards_status,flg)

		oval_score += score[0]
		cross_score += score[1]
		print cross_score,oval_score
	
		if(flg == 'o'):
			return oval_score - cross_score
		else : 
			return cross_score - oval_score

	def minmax(self,cur_board,old_move,flg,dep,turn):
		flg2 = 'o'
		if flg == 'o' : 
			flg2 = 'x'
		if dep == gdep	 :
			return self.heuristic(cur_board,flg) 
		mn = -inf
		mx = inf
		rx = 0
		ry = 0
		rz = 0
		if allowed_cells is not None: 
			for i in range(len(allowed_cells)):
				x = allowed_cells[i][0]
				y = allowed_cells[i][1]
				z = allowed_cells[i][2]
				cur_board.big_boards_status[x][y][z]=flg 
				sty = y/3
				stz = z/3
				for i in range(3):
					for j in range(3):
						temp_board2[i][j]= cur_board.big_boards_status[x][3*sty+i][3*stz+j]
				temp_board2 = ([['-' for i in range(3)] for j in range(3)])
				another_turn = 0
				val2 = self.check_small_board_won(temp_board2)
				if val2 != 0 :
					another_turn = 1

				val = 0 
				if(another_turn == 1 ):
					val = self.minmax(cur_board,(x,y,z),flg,dep+1,turn)
				else : 
					val = self.minmax(cur_board,(x,y,z),flg2,dep+1,1-turn)
			allowed_cells = self.find_valid_move_cells(cur_board,old_move)

			if turn % 2 == 1 :
				if val < mn:
					mn = val
					rx = x 
					ry = y
					rz = z
			else : 
				if val > mx:
					mx = val
					rx = x 
					ry = y
					rz = z			
			cur_board.big_boards_status[x][y][z]='-'
			cur_board.small_boards_status[x][sty][stz] = '-'					
			return (mnx,mny,mnz)

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