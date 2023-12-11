#!/usr/bin/python3
import sys
import random
import time

class Conway:
	def __init__(self,dim):
		self.dim = dim
		self.table =  [[ '0' for x in range(self.dim+2)] for y in range(self.dim+2)] # init game

		# fill the 'true' matrix
		for i in range(1,dim+1):
			for y in range(1,dim+1):
				self.table[i][y] = str(random.randrange(0,2)) 


	def print_mat(self):
	    for row in self.table:
	        for el in row:
	            print(f"{el} ",end="")
	        print("\n")

	def nb_neighbours(self,table,i_case,y_case):
		cpt = 0
		for i in range(i_case-1,i_case+2):
			for y in range(y_case-1,y_case+2):
				if i != i_case or y != y_case:
					if table[i][y] == '1':
						cpt+=1
		return cpt

	def update(self):
		table_prev = self.table
		table_next = [['0' for x in range(self.dim+2)] for y in range(self.dim+2)]

		for i in range(1,self.dim+1):
			for y in range(1,self.dim+1):
				case = table_prev[i][y]
				nb_voisin = self.nb_neighbours(table_prev,i,y)

				if case == '0':
					if nb_voisin == 3:
						table_next[i][y] = '1'
					else:
						table_next[i][y] = case
				else:
					if nb_voisin == 2 or nb_voisin == 3:
						table_next[i][y] = '1'
					else:
						table_next[i][y] = '0'


		self.table = table_next


if len(sys.argv) != 2:
	print("usage : conway.py x")
else:
	dim = int(sys.argv[1])

	game = Conway(dim)
	game.print_mat()

	while True:
		game.update()
		print("-----------------------------------")
		game.print_mat()
		time.sleep(0.5)