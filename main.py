from subprocess import *
import sys
import threading
import json
import re
import command
from logging import Logger
from taskmaster import taskmaster

def interface(data):
	try:
		t = taskmaster(data, )
		t.start()

		while (True):
			cmd = input("Taskmaster--> ")
			cmd = cmd.strip()
			check = command.check_command(cmd, t)
			if (check == -1):
				break
			if (check == 1):
				print("Unknown command: " + cmd)

		t.join()
	except:
		print("An interaction error occured")

def loadconf(name):
	try:
		with open (name, "r") as data_file:
			filedata = json.load(data_file)
			return filedata
	except:
		print("Error: Invalid config file!")
		print("Config file must be a valid JSON file")

def main():
	try:
		filedata = loadconf(sys.argv[1])
		interface(filedata['programs'])
	except:
		pass

if (__name__ == '__main__'):
	if (len(sys.argv) > 1):
		main()
	else:
		print("Warning: No config file given")
		print("Cannot run Taskmaster without config file")