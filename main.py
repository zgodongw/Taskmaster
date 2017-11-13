from subprocess import *
import sys
import threading
import json
import re
from logging import Logger
from taskmaster import taskmaster

def check_command(name, t):
	if ("kill" in name):
		sub = name.split()
		if (len(sub) == 2):
			t.kill(sub[1], out=True)
		else:
			print("Syntax Error!\nUsage: kill <program>")
		return 0

	if ("stop" in name):
		sub = name.split()
		if (len(sub) == 2):
			t.kill(sub[1], stop=True)
		else:
			print("Syntax Error!\nUsage: start <program>")
		return 0

	if name == "status":
		t.isRunning()
		return 0

	if name == "clear":
		print("\33[H\33[2J", end="")
		return 0
	
	if ("restart" in name):
		sub = name.split()
		if (len(sub) > 1):
			t.restarting(sub[1])
		else:
			print("Syntax Error!\nUsage: restart <program>")
		return 0
	elif ("start" in name):
		sub = name.split()
		if (len(sub) > 1):
			t.starting(sub[1])
		else:
			print("Syntax Error!\nUsage: start <program>")
		return 0

	if (name == "exit" or name == "quit"):
		t.kill('all')
		return -1
	if not name.strip():
		return 12

	return 1

def interface(data):
	try:
		t = taskmaster(data, )
		t.start()

		while (True):
			command = input("Taskmaster--> ")
			command = command.strip()
			check = check_command(command, t)
			if (check == -1):
				break
			if (check == 1):
				print("Unknown command: " + command)
	
		t.join()
	except:
		print("An unkown error occured")

def main():
	try:
		with open (sys.argv[1], "r") as data_file:
			filedata = json.load(data_file)
			data_file.close()
	
		interface(filedata['programs'])
	except:
		print("Error: Invalid config file!")
		print("Config file must be a valid JSON file")

if (__name__ == '__main__'):
	if (len(sys.argv) > 1):
		main()
	else:
		print("Warning: No config file given")
		print("Cannot run Taskmaster without config file")
