import sys
import random
import signal
import time
import copy
# from simulator import BigBoard
inf = 100000000000000000
inf2 = 10000000000000
class MyPlayer2():
	
	def __init__(self):
		pass
		self.empty_small_board = "---------"
		self.small_board_score = {}
		self.small_board_score_d = {}
		self.preprocess(self.empty_small_board)
		self.preprocess_d(self.empty_small_board)

	def change(self,s,i,c):
		s = s[:i] + c + s[i+1:]
		return s
	def check_small_board_won_matrix(self,bs):
		for i in range(3):
			if (bs[i][0] == bs[i][1] == bs[i][2]) and (bs[i][0] == 'o'):
				return 50
			if (bs[i][0] == bs[i][1] == bs[i][2]) and (bs[i][0] == 'x'):
				return -50
			if (bs[0][i] == bs[1][i] == bs[2][i]) and (bs[0][i] == 'o'):
				return 50
			if (bs[0][i] == bs[1][i] == bs[2][i]) and (bs[0][i] == 'x'):
				return -50
		#checking for diagonal patterns
		if (bs[0][0] == bs[1][1] == bs[2][2]) and (bs[0][0] == 'o'):
			return 50
		if (bs[0][0] == bs[1][1] == bs[2][2]) and (bs[0][0] == 'x'):
			return -50
		#diagonal 2
		if (bs[0][2] == bs[1][1] == bs[2][0]) and (bs[0][2] == 'o'):
			return 50
		if (bs[0][2] == bs[1][1] == bs[2][0]) and (bs[0][2] == 'x'):
			return -50
		return 0
	def check_small_board_won_str(self,bs):
		for i in range(3):
			if (bs[3*i] == bs[3*i+1] == bs[3*i+2]) and (bs[3*i] == 'o'):
				return 50
			if (bs[3*i] == bs[3*i+1] == bs[3*i+2]) and (bs[3*i] == 'x'):
				return -50
			if (bs[i] == bs[i+3] == bs[i+6]) and (bs[i] == 'o'):
				return 50
			if (bs[i] == bs[i+3] == bs[i+6]) and (bs[i] == 'x'):
				return -50
		#checking for diagonal patterns
		if (bs[0] == bs[4] == bs[8]) and (bs[0] == 'o'):
			return 50
		if (bs[0] == bs[4] == bs[8]) and (bs[0] == 'x'):
			return -50
		#diagonal 2
		if (bs[2] == bs[4] == bs[6]) and (bs[2] == 'o'):
			return 50
		if (bs[2] == bs[4] == bs[6]) and (bs[2] == 'x'):
			return -50
		return 0
	def preprocess(self,bs):
		x = self.check_small_board_won_str(bs)
		if x == 50 : 
 			self.small_board_score[bs]=(1,0,0)
 			return (1,0,0)
 		if x == -50 :
 			self.small_board_score[bs]=(0,1,0)
 			return (0,1,0)
		#check if board is already complete
		flag = 0
		for i in range(9):
				if bs[i] != '-' :
					flag = flag + 1
		if flag == 9 :
			self.small_board_score[bs]= (0,0,1)
			return (0,0,1)

		if bs in self.small_board_score:
			return self.small_board_score[bs]
		ret0=0
		ret1=0
		ret2=0

		for i in range(9):
			if bs[i] == '-':
				bs = self.change(bs,i,'o')
				val = self.preprocess(bs)
				ret0+=val[0]
				ret1+=val[1]
				ret2+=val[2]
				bs = self.change(bs,i,'x')
				val = self.preprocess(bs)
				ret0+=val[0]
				ret1+=val[1]
				ret2+=val[2]
				bs = self.change(bs,i,'-')
		self.small_board_score[bs] = (ret0,ret1,ret2)
		return (ret0,ret1,ret2)
	
	def preprocess_d(self,bs):
		x = self.check_small_board_won_str(bs)
		if x == 50 : 
 			self.small_board_score_d[bs]=(1,0,0)
 			return (1,0,0)
 		if x == -50 :
 			self.small_board_score_d[bs]=(0,1,0)
 			return (0,1,0)
		#check if board is already complete
		flag = 0
		for i in range(9):
				if bs[i] != '-'  :
					flag = flag + 1
		if flag == 9 :
			self.small_board_score_d[bs]= (0,0,1)
			return (0,0,1)

		if bs in self.small_board_score_d:
			return self.small_board_score_d[bs]
		ret0=0
		ret1=0
		ret2=0
		for i in range(9):
			if bs[i] == '-':
				bs = self.change(bs,i,'o')
				val = self.preprocess_d(bs)
				ret0+=val[0]
				ret1+=val[1]
				ret2+=val[2]
				bs = self.change(bs,i,'x')
				val = self.preprocess_d(bs)
				ret0+=val[0]
				ret1+=val[1]
				ret2+=val[2]
				bs = self.change(bs,i,'d')
				val = self.preprocess_d(bs)
				ret0+=val[0]
				ret1+=val[1]
				ret2+=val[2]
				bs = self.change(bs,i,'-')
		self.small_board_score_d[bs] = (ret0,ret1,ret2)
		return (ret0,ret1,ret2)


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

	def print_board(self,board):
		# for printing the state of the board
		for i in range(9):
			if i%3 == 0:
				print
			for k in range(2):
				for j in range(9):
					if j%3 == 0:
						print "",
					print board.big_boards_status[k][i][j],
				if k==0:
					print "   ",
			print
		print

		for i in range(3):
			for k in range(2):
				for j in range(3):
					print board.small_boards_status[k][i][j],
				if k==0:
					print "  ",
			print
		print
		print



	def heuristic(self,board,flg):

		cross_score = 0
		oval_score = 0
		# print(board)
		factor=1000
		for k in range(2):
			for i in range(3):
				for j in range(3):
					temp_board = ""
					for x in range(3):
						for y in range(3):
							temp_board +=board.big_boards_status[k][3*i+x][3*j+y]
					score = self.small_board_score[temp_board]
					total = score[0] + score[1] + score[2]
					oval_val = float(score[0])/total
					cross_val = float(score[1])/total
					oval_score += float(oval_val)*factor
					cross_score += float(cross_val)*factor


		for k in range(2):
			temp_board = ""
			for i in range(3):
				for j in range(3):
					temp_board+=board.small_boards_status[k][i][j]
			score = self.small_board_score[temp_board]
			total = score[0] + score[1] + score[2]
			oval_val= float(score[0])/total
			cross_val= float(score[1])/total
			oval_score += float(oval_val)*factor*100.0
			cross_score += float(cross_val)*factor*100.0

		return (oval_score,cross_score)

	def minmax(self,cur_board,old_move,flg,dep):
		flg2 = 'o'
		if flg == 'o' : 
			flg2 = 'x'
		if dep == 0	 :
			return self.heuristic(cur_board,flg) 
		mx = -inf
		rx = 0
		ry = 0
		rz = 0
		ret = (0,0)
		allowed_cells = self.find_valid_move_cells(cur_board,old_move)
		if allowed_cells is not None:
			for i in range(len(allowed_cells)): 
				x = allowed_cells[i][0]
				y = allowed_cells[i][1]
				z = allowed_cells[i][2]
				cur_board.big_boards_status[x][y][z]=flg 
				sty = y/3
				stz = z/3
				temp_board = ([['-' for i in range(3)] for j in range(3)])
				for i in range(3):
					for j in range(3):
						temp_board[i][j] = cur_board.big_boards_status[x][3*sty+i][3*stz+j]
			
				another_turn = 0	
			
				val2 = self.check_small_board_won_matrix(temp_board)
				if val2 != 0 :
					cur_board.small_boards_status[x][sty][stz] = flg
					another_turn = 1
				
				arnav = self.check_small_board_won_matrix(cur_board.big_boards_status[x]) 
				
				if arnav != 0  :
					cur_board.big_boards_status[x][y][z]= '-'
					cur_board.small_boards_status[x][sty][stz] = '-'					
					if dep == self.gdep:
						return (x,y,z)
					elif flg == 'o': 
						return (inf2,0)
					else :
						return (0,inf2)
				
				val = (0,0) 
				
				if another_turn == 1 :
					val = self.minmax(cur_board,(x,y,z),flg,dep-1)
				else : 
					val = self.minmax(cur_board,(x,y,z),flg2,dep-1)
				cur_board.big_boards_status[x][y][z]= '-'
				cur_board.small_boards_status[x][sty][stz] = '-'					
				
				score = val[0] - val[1]
				if flg == 'o' :
					if score > mx:
						mx = score
						rx = x
						ry = y
						rz = z	
						ret = val
				else :
					score = -score
					if score > mx:
						mx = score
						rx = x
						ry = y
						rz = z						 
						ret = val
		
		if dep == self.gdep:
			return (rx,ry,rz)
		else :
			return ret

	def move(self,board,old_move,flg):
		self.st_time = time.time()
		cur_board = copy.deepcopy(board)
		
		allowed_cells = self.find_valid_move_cells(cur_board,old_move)
		for i in range(len(allowed_cells)):
			x = allowed_cells[i][0]
			y = allowed_cells[i][1]
			z = allowed_cells[i][2]			
			cur_board.big_boards_status[x][y][z]=flg 
			sty = y/3
			stz = z/3
			temp_board = ([['-' for i in range(3)] for j in range(3)])
			for i in range(3):
				for j in range(3):
					temp_board[i][j]= cur_board.big_boards_status[x][3*sty+i][3*stz+j]
			another_turn = 0
			val2 = self.check_small_board_won_matrix(temp_board)
			if val2 != 0 :
				return(x,y,z)
			cur_board.big_boards_status[x][y][z]='-' 
		
		self.gdep = 3
		cur_move = self.minmax(cur_board,old_move,flg,3)
		x = cur_move[0]
		y = cur_move[1]
		z = cur_move[2]
		return (x,y,z)


# board = BigBoard()
player = MyPlayer2()
# player.heuristic(board)