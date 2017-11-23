from subprocess import *
import time
import colors
import os

def main(me=False):
	if me == True:
		print("{}testing{}{} Hello{}".format(colors.GREEN, colors.RESET, colors.BOLD, colors.RESET))
	print("done")

main(me=True)