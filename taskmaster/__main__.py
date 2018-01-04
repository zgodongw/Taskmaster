from subprocess import *
import sys, signal
import threading
import json
import re
import command
import logging
import colors
from taskmaster import taskmaster

logging.basicConfig(filename='Taskmaster.log', level=logging.INFO, format='%(levelname)s:%(asctime)s:%(message)s')

def interface(data):
	#try:
		logging.info('Starting taskmaster')
		t = taskmaster(data,)
		t.start()

		signal.signal(signal.SIGCHLD, t.checkAll)
		while (True):
			cmd = input("{}{}[Taskmaster]$ {}".format(colors.BOLD, colors.GREEN, colors.RESET))
			cmd = cmd.strip()
			check = command.check_command(cmd, t)
			if (check == -1):
				logging.info('Taskmaster finished')
				break
			if (check == 1):
				print("Unknown command: " + cmd)
	#except:
	#	print("An Taskmaster shell error occured")
	#finally:
		t.join()

def loadConf(name):
	try:
		with open (name, "r") as data_file:
			filedata = json.load(data_file)
			return filedata
	except:
		print("Error: Invalid config file!")
		print("Config file must be a valid JSON file")

def main():
	#try:
		filedata = loadConf(sys.argv[1])
		interface(filedata['programs'])
	#except:
	#	pass

if (__name__ == '__main__'):
	if (len(sys.argv) > 1):
		main()
	else:
		print("Warning: No config file given")
		print("Cannot run Taskmaster without config file")

'''
NUMBER OF PROCESSES HAS AN ERROR ON RELOAD
'''