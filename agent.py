import sys
import random
import signal
import time
import copy

class MyPlayer():


    def __init__(self):
    	pass

    def print_board(self):
	# for printing the state of the board
		print '==============Board State=============='
		for i in range(16):
			if i%4 == 0:
				print
			for j in range(16):
				if j%4 == 0:
					print "",
				print self.board_status[i][j],
			print
		print

		print '==============Block State=============='
		for i in range(4):
			for j in range(4):
				print self.block_status[i][j],
			print
		print '======================================='
		print
		print

    def get_available_moves(self):
	    self.available_moves = [[[] for j in range(4)] for i in range(4)]
	    for i in range(16):
	        for j in range(16):
	            if self.board_status[i][j] == '-' and self.block_status[i/4][j/4] == '-':
	                self.available_moves[i/4][j/4].append((i,j))
	    return

    def find_valid_move_cells(self, old_move):
        allowed_cells = []
        allowed_block = [old_move[0]%4, old_move[1]%4]

        if old_move != (-1,-1) and self.block_status[allowed_block[0]][allowed_block[1]] == '-':
            for i in range(4*allowed_block[0], 4*allowed_block[0]+4):
                for j in range(4*allowed_block[1], 4*allowed_block[1]+4):
                    if self.board_status[i][j] == '-':
                        allowed_cells.append((i,j))
        else:
            for i in range(16):
                for j in range(16):
                    if self.board_status[i][j] == '-' and self.block_status[i/4][j/4] == '-':
                        allowed_cells.append((i,j))
        return allowed_cells

    # def move(self, board, old_move, flag):

Superbot = MyPlayer()