	def check_small_board_score(self,bs):

		# print(bs)
		cross_score = 0
		oval_score = 0
		# print(board)
		a6 = 50 #diagnoal corner corner
		a5 = 40
		a4 = 60
		a3 = 30
		a2 = 20
		a1 = 10
		val = self.check_small_board_won(bs)
		if val == 50 :
			return (200,0)
		elif val == -50 :
			return (0,200) 

		# center and corner  
		if bs[1][1] == 'x':
			if bs[0][0] == 'x' :  
				cross_score += a4
			if bs[0][2] == 'x' :
				cross_score += a4
			if bs[2][0] == 'x' :  
				cross_score += a4
			if bs[2][2] == 'x' :
				cross_score += a4

		if bs[1][1] == 'o':
			if bs[0][0] == 'o' :
				oval_score += a4
			if bs[0][2] == 'o' :
				oval_score += a4
			if bs[2][0] == 'o' : 
				oval_score += a4
			if bs[2][2] == 'o' :
				oval_score += a4


		# center and middle 
		if bs[1][1] == 'x':
			if bs[0][1] == 'x': 
				cross_score += a2
			if bs[1][0] == 'x': 
				cross_score += a2
			if bs[1][2] == 'x': 
				cross_score += a2
			if bs[2][1] == 'x':
				cross_score += a2


		if bs[1][1] == 'o':
			if bs[0][1] == 'o': 
				oval_score += a2
			if bs[1][0] == 'o': 
				oval_score += a2
			if bs[1][2] == 'o': 
				oval_score += a2
			if bs[2][1] == 'o':
				oval_score += a2


		#corner and middle
		if bs[0][1] == 'x':
			if bs[0][0] == 'x' :
				cross_score += a1
			if bs[0][2] == 'x' :
				cross_score += a1

		if bs[2][1] == 'x':
			if bs[2][0] == 'x': 
				cross_score += a1
			if bs[2][2] == 'x':
				cross_score += a1

		if bs[0][1] == 'o':
			if bs[0][0] == 'o': 
				oval_score += a1
			if bs[0][2] == 'o':
				oval_score += a1

		if bs[2][1] == 'o':
			if bs[2][0] == 'o': 
				oval_score += a1
			if bs[2][2] == 'o':
				oval_score += a1

		#vertical
		if bs[1][0] == 'x':
			if bs[0][0] == 'x' :
				cross_score += a1
			if bs[2][0] == 'x':
				cross_score += a1

		if bs[1][2] == 'x':
			if bs[0][2] == 'x': 
				cross_score += a1
			if bs[2][2] == 'x':
				cross_score += a1

		if bs[1][0] == 'o':
			if bs[0][0] == 'o': 
				oval_score += a1
			if bs[2][0] == 'o':
				oval_score += a1

		if bs[1][2] == 'o':
			if bs[0][2] == 'o':
				oval_score += a1
			if bs[2][2] == 'o':
				oval_score += a1
		#corner-corner
		if bs[0][0] == 'x':
			if bs[2][2] == 'x':
				cross_score += a6
			if bs[0][2] == 'x':
				cross_score += a5
			if bs[2][0] == 'x':
				cross_score += a5
		
		if bs[0][2] == 'x':
			if bs[2][0] == 'x':
				cross_score += a6
			if bs[2][2] == 'x':
				cross_score += a5

		if bs[2][0] == 'x':
			if bs[2][2] == 'x':
				cross_score += a5

		if bs[0][0] == 'o':
			if bs[2][2] == 'o':
				oval_score += a6
			if bs[0][2] == 'o':
				oval_score += a5
			if bs[2][0] == 'o':
				oval_score += a5
		
		if bs[0][2] == 'o':
			if bs[2][0] == 'o':
				oval_score += a6
			if bs[2][2] == 'o':
				oval_score += a5

		if bs[2][0] == 'o':
			if bs[2][2] == 'o':
				oval_score += a5
		return (oval_score,cross_score)

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