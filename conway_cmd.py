#!/usr/bin/python3
import sys
from conway import *


if len(sys.argv) != 3:
	print("usage : conway_cmd.py x mode")
else:
	dim = int(sys.argv[1])
	mode = str(sys.argv[2])

	game = Conway(dim)
	game.print_mat()

	if mode == "iter":
		i=1
		while True:
			game.update_iter()
			print(f"round n° {i}-----------------------------------")
			game.print_mat()
			time.sleep(1)
			i+=1
	elif mode == "thread_one":
		i=1
		while True:
			game.update_thread_one()
			print(f"round n° {i}-----------------------------------")
			game.print_mat()
			time.sleep(1)
			i+=1
	elif mode == "thread_two":
		#q3
		game.thread_two()

	
	