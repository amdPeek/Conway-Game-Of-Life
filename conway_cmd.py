#!/usr/bin/python3
import sys
from conway import *


if len(sys.argv) != 2:
	print("usage : conway_cmd.py x")
else:
	dim = int(sys.argv[1])

	game = Conway(dim)
	game.print_mat()

	while True:
		game.update()
		print("-----------------------------------")
		game.print_mat()
		time.sleep(0.5)