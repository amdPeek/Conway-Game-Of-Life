#!/usr/bin/python3

import random
import threading
import time


class Barriere:
    def __init__(self, n, Conway):

        self.n = n
        self.waiting_threads = 0
        self.lock_barriere = threading.Lock()
        self.condition = threading.Condition(self.lock_barriere)
        self.conway = Conway

    def wait(self):
        with self.lock_barriere:
            self.waiting_threads+=1
            if self.waiting_threads == self.n:
                self.waiting_threads = 0 
                self.condition.notify_all()
                self.conway.table = self.conway.table_next 
                self.conway.table_next = [['0' for x in range(self.conway.dim+2)] for y in range(self.conway.dim+2)]
                self.conway.round +=1 
                print(f"------------------- round n° {self.conway.round} -------------------")
                self.conway.print_mat()
            else:
                self.condition.wait()

class Conway:
	def __init__(self,dim):
		self.dim = dim
		self.table =  [[ '0' for x in range(self.dim+2)] for y in range(self.dim+2)] # init game
		self.table_next = [['0' for x in range(self.dim+2)] for y in range(self.dim+2)]
		self.lock = threading.Lock()

		#pour la version q.3
		self.threads_list = []
		self.barriere = Barriere(self.dim*self.dim,self)
		self.round = 1

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

	def thread_target_one(self,i,y,table_prev):

		
		case = table_prev[i][y]
		nb_voisin = self.nb_neighbours(table_prev,i,y)

		with self.lock:
			if case == '0':
				if nb_voisin == 3:
					self.table_next[i][y] = '1'
				else:
					self.table_next[i][y] = case
			else:
				if nb_voisin == 2 or nb_voisin == 3:
					self.table_next[i][y] = '1'
				else:
					self.table_next[i][y] = '0'

	def update_thread_one(self):

		l_thread = []
		for i in range(1,self.dim+1):
			for y in range(1,self.dim+1):
				l_thread.append(threading.Thread(target=self.thread_target_one,args=(i,y,self.table,)))

		#lancement des threads
		for t in l_thread:
			t.start()
			t.join()

		self.table = self.table_next
		self.table_next = [['0' for x in range(self.dim+2)] for y in range(self.dim+2)]

	def thread_target_two(self,i,y,table_prev):
		
		case = table_prev[i][y]
		nb_voisin = self.nb_neighbours(table_prev,i,y)

		with self.lock:
			if case == '0':
				if nb_voisin == 3:
					self.table_next[i][y] = '1'
				else:
					self.table_next[i][y] = case
			else:
				if nb_voisin == 2 or nb_voisin == 3:
					self.table_next[i][y] = '1'
				else:
					self.table_next[i][y] = '0'

		self.barriere.wait()
		
		time.sleep(1)
		
		
		self.thread_target_two(i,y,self.table)

	def thread_two(self):

		for i in range(1,self.dim+1):
			for y in range(1,self.dim+1):
				self.threads_list.append(threading.Thread(target=self.thread_target_two,args=(i,y,self.table,)))

		for t in self.threads_list:
			t.start()
		
		for t in self.threads_list:
			t.join()

		

	def update_iter(self):
		table_prev = self.table
		

		for i in range(1,self.dim+1):
			for y in range(1,self.dim+1):
				case = table_prev[i][y]
				nb_voisin = self.nb_neighbours(table_prev,i,y)

				if case == '0':
					if nb_voisin == 3:
						self.table_next[i][y] = '1'
					else:
						self.table_next[i][y] = case
				else:
					if nb_voisin == 2 or nb_voisin == 3:
						self.table_next[i][y] = '1'
					else:
						self.table_next[i][y] = '0'


		self.table = self.table_next
		self.table_next = [['0' for x in range(self.dim+2)] for y in range(self.dim+2)]
	
