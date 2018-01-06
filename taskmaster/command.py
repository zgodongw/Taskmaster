import colors
import logging
import cmd
import signal
from subprocess import *

logging.basicConfig(filename='Taskmaster.log', level=logging.INFO, format='%(levelname)s:%(asctime)s:%(message)s')

class command(cmd.Cmd):
	intro = None
	prompt = "{}{}[Taskmaster]$ {}".format(colors.BOLD, colors.GREEN, colors.RESET)
	file = None
	user = str()
	t = None

	def preloop(self):
		self.t.start()
		signal.signal(signal.SIGCHLD, self.t.checkAll)
	
	def default(self, arg):
		print("Error: Unknown command: " + arg)
	
	def do_help(self, arg):
		try:
			less = Popen(['less', 'help.txt'])
			less.wait()
		except:
			with open("help.txt", 'r') as f_help:
				for line in f_help:
					print(line)

	def do_status(self, arg):
		self.t.isRunning()
	
	def do_clear(self, arg):
		print(colors.CLEAR, end="")

	def do_kill(self, arg):
		sub = arg.split()
		if (len(sub) == 1):
			self.t.kill(sub[0], out=True)
		elif (len(sub) == 2):
			self.t.kill(sub[0],pid=int(sub[1]), out=True)
		else:
			print("Syntax Error!\nUsage: kill <program> [<pid>]")
	
	def do_stop(self, arg):
		sub = arg.split()
		if (len(sub) == 1):
			self.t.kill(sub[0], stop=True)
		elif (len(sub) == 2):
			self.t.kill(sub[0],pid=int(sub[1]), stop=True)
		else:
			print("Syntax Error!\nUsage: kill <program> [<pid>]")

	def do_start(self, arg):
		if arg:
			self.t.starting(arg)
		else:
			print("Syntax Error!\nUsage: start <program>")
	
	def do_restart(self, arg):
		if self.user == "God":
			sub = arg.split()
			if (len(sub) == 1):
				self.t.restarting(sub[0])
			elif (len(sub) == 2):
				self.t.restarting(sub[0],rpid=int(sub[1]))
			else:
				print("Syntax Error!\nUsage: restart <program> [<pid>]")
		else:
			print('Taskmaster: Command not available to humans : restart\nSee help.')
	
	def do_reload(self, arg):
		if self.user == "God":
			sub = arg.split()
			if (len(sub) == 1):
				responce = input("Are you sure? (y/n) ")
				if (responce == 'y' or responce == 'yes'):
					logging.info('Attemping to reload.')
					print("Reloading...")
					self.t.reloadConf(sub[0])
					print("Done!")
					logging.info('Reload attempt complete.')
			else:
				print("Syntax Error!\nUsage: start <program>")
		else:
			print('Taskmaster: Command not available to humans : reload\nSee help.')

	def do_exit(self, arg):
		self.t.kill('all')
		return True
