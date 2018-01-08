from subprocess import *
import sys, signal
import threading
import json
import re
from command import command
import logging
import colors
from taskmaster import taskmaster
from bonus import *
import optparse

logging.basicConfig(filename='Taskmaster.log', level=logging.INFO, format='%(levelname)s:%(asctime)s:%(message)s')

def interface(data, user):
	try:
		logging.info('Starting taskmaster as {}'.format(user))
		t = taskmaster(data,)

		task = command()
		task.user = user
		task.t = t
		task.cmdloop()

	except:
		print("An Taskmaster shell error occured")
	finally:
		t.join()


def loadConf(name):
	try:
		with open (name, "r") as data_file:
			filedata = json.load(data_file)
			return filedata
	except:
		print("Error: Invalid config file!")
		print("Config file must be a valid JSON file")

def main(*args):
	try:
		filedata = loadConf(args[0])
		interface(filedata['programs'], args[1])
		if args[2] != None:
			sendLogReport(args[2])
	except:
		pass
if (__name__ == '__main__'):
	parser = optparse.OptionParser("Usage: -c <config file name>\n -u <User: either God or human>\n -e <email>")

	parser.add_option('-c', dest='configName', help="Config name", type="string")
	parser.add_option('-u', dest='userName', help="User either God or human", type="string")
	parser.add_option('-e', dest='emailAddress', help="Email Address for log report", type="string")

	(option, args) = parser.parse_args()

	if (option.configName != None):
		main(option.configName, getUser(option.userName), option.emailAddress)
	else:
		print("Warning: No config file given")
		print("Cannot run Taskmaster without config file")

'''
NUMBER OF PROCESSES HAS AN ERROR ON RELOAD AND RESTART
'''