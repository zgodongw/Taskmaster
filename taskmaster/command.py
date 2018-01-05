import colors
import logging
from subprocess import *

logging.basicConfig(filename='Taskmaster.log', level=logging.INFO, format='%(levelname)s:%(asctime)s:%(message)s')



def printHelp():
	try:
		less = Popen(['less', 'help.txt'])
		less.wait()
	except:
		with open("help.txt", 'r') as f_help:
			for line in f_help:
				print(line)

def check_command(name, t, user):

	humanCommands = ['kill', 'start', 'stop', 'exit', 'quit','clear', 'help', 'status']

	if user == 'human':
		sub = name.split()
		if sub[0] not in humanCommands:
			return 42

	if ("kill" in name):
		sub = name.split()
		if (len(sub) == 2):
			t.kill(sub[1], out=True)
		elif (len(sub) == 3):
			t.kill(sub[1],pid=int(sub[2]), out=True)
		else:
			print("Syntax Error!\nUsage: kill <program> [<pid>]")
		return 0

	if ("stop" in name):
		sub = name.split()
		if (len(sub) == 2):
			t.kill(sub[1], stop=True)
		elif (len(sub) == 3):
			t.kill(sub[1],pid=int(sub[2]), stop=True)
		else:
			print("Syntax Error!\nUsage: stop <program> [<pid>]")
		return 0

	if name == "status":
		t.isRunning()
		return 0

	if name == "help":
		printHelp()
		return 0

	if name == "clear":
		print(colors.CLEAR, end="")
		return 0

	if ("reload" in name):
		sub = name.split()
		if (len(sub) == 2):
			responce = input("Are you sure? (y/n) ")
			if (responce == 'y' or responce == 'yes'):
				logging.info('Attemping to reload.')
				print("Reloading...")
				t.reloadConf(sub[1])
				print("Done!")
				logging.info('Reload attempt complete.')
		else:
			print("Syntax Error!\nUsage: start <program>")
		return 0

	if ("restart" in name):
		sub = name.split()
		if (len(sub) > 1):
			t.restarting(sub[1])
		elif (len(sub) == 3):
			t.restarting(sub[1],rpid=int(sub[2]))
		else:
			print("Syntax Error!\nUsage: restart <program> [<pid>]")
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