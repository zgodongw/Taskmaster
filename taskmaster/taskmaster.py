from subprocess import *
import sys
import os, signal
import threading
import json
import re
import colors
import logging

logging.basicConfig(filename='Taskmaster.log', level=logging.INFO, format='%(levelname)s:%(asctime)s:%(message)s')

class taskmaster(threading.Thread):
	def __init__(self, data):
		threading.Thread.__init__(self)
		self.daemon = True
		self.data = data
		self.prognames = list(self.data.keys())
		self.proglist = {}

	def setKeys(self):
		for name in self.prognames:
			try:
				if 'numprocs' not in self.data[name]:
					self.data[name]['numprocs'] = 1
				if 'autostart' not in self.data[name]:
					self.data[name]['autostart'] = False
				if 'stdout' not in self.data[name]:
					self.data[name]['stdout'] = None
				if 'stderr' not in self.data[name]:
					self.data[name]['stderr'] = None
				if 'autorestart' not in self.data[name]:
					self.data[name]['autorestart'] = "never"
				if 'startretries' not in self.data[name]:
					self.data[name]['startretries'] = 0
				if 'starttime' not in self.data[name]:
					self.data[name]['starttime'] = 0
				if 'stoptime' not in self.data[name]:
					self.data[name]['stoptime'] = 0
				if 'stopsignal' not in self.data[name]:
					self.data[name]['stopsignal'] = "HUP"
				if 'exitcodes' not in self.data[name]:
					self.data[name]['exitcodes'] = [0]
				if 'workingdir' not in self.data[name]:
					self.data[name]['workingdir'] = './'
				if 'umask' not in self.data[name]:
					self.data[name]['umask'] = 22
				if 'env' not in self.data[name]:
					self.data[name]['env'] = {}
			except:
				pass

	def getSignal(self, s):
		s = s.upper()
		if s == "TERM":
			return signal.SIGTERM
		if s == "HUP":
			return signal.SIGHUP
		if s == "INT":
			return signal.SIGINT
		if s == "QUIT":
			return signal.SIGQUIT
		if s == "KILL":
			return signal.SIGKILL
		if s == "USR1":
			return signal.SIGUSR1
		if s == "USR2":
			return signal.SIGUSR2
		raise signal.UnknowSignalError()

	def run(self):
		self.setKeys()
		for prog in self.prognames:
			if prog not in self.proglist:
				self.proglist[prog] = None
			if (self.data[prog]['autostart'] == True):
				self.starting(prog)
		
	def	kill(self, string, pid=None, stop=False, out=False):
		for name in self.prognames:
			for x in range(self.data[name]['numprocs']):
				if ((name == string or string == "all") and (self.proglist[name] != None)):
					if (pid == self.proglist[name][x][1] or pid == None):
						if stop == False:
							try:
								os.kill(self.proglist[name][x][1], self.getSignal(self.data[name]['stopsignal']))
							except:
								pass
						elif stop == True:
							kill = self.proglist[name][x][0].kill()
						if out == True:
							print(name + " has been killed!")
	
	def	restarting(self, string, rpid=None, retry=0):
		try:
			self.kill(string, pid=rpid)
			self.starting(string, run=True, retry=retry)
		except:
			print("Couldn't restart the process. please start it")

	def reloadConf(self, name):
		try:
			with open (name, "r") as data_file:
				filedata = json.load(data_file)
			self.data = None
			self.data = filedata['programs']
			self.prognames = list(self.data.keys())
			self.run()
		except:
			print("Error: Invalid config file!")
			print("Config file must be a valid JSON file")

	def setenv(self, name):
		for key in self.data[name]['env']:
			os.environ[key] = self.data[name]['env'][key]

	def	starting(self, string, run=False, retry=0):
		for name in self.prognames:
			try:
				outfile		= open(self.data[name]['stdout'], "a+")
			except:
				outfile		= PIPE
			try:
				errorfile	= open(self.data[name]['stderr'], "a+")
			except:
				errorfile	= PIPE 

			try:
				os.umask(self.data[name]['umask'])
				self.setenv(name)
			except:
				pass
			wkdir = self.data[name]['workingdir']
			dictpointer = {}
			try:
				if (name == string and (self.proglist[name] == None or run == True)):
					for x in range(self.data[name]['numprocs']):
						if (name == string):			
							tostart = re.split('\ (?=-)', self.data[name]['cmd'])
							logging.info('Starting {}'.format(tostart))
							Pobj = Popen(tostart, stdout=outfile, stderr=errorfile, cwd=wkdir)
							pid = Pobj.pid
							dictpointer[x] = [Pobj, pid, retry]
						if (dictpointer != {}):
							self.proglist[name] = dictpointer
			except:
				print("Error: couldn't open {}".format(name))
			finally:
				try:
					outfile.close()
					errorfile.close()
				except:
					pass
	def checkAll(self, signal, frame):
		for name in self.prognames:
			if (self.proglist[name] == None):
				continue
			for x in range(self.data[name]['numprocs']):
				varretry = self.proglist[name][x][2]
				pobj = self.proglist[name][x][0]
				varpid = self.proglist[name][x][1]
				status = pobj.poll()
				for codes in self.data[name]['exitcodes']:
					if status == codes or status == -9:
						logging.info('{} finished successfully.'.format(name))
						break
				else:
					logging.info('{} stopped unexpectedly.'.format(name))
					if self.data[name]['autorestart'] is not "never":
						if varretry < self.data[name]['startretries']:
							logging.info('Restarting {}'.format(name))
							self.restarting(name, rpid=varpid, retry=varretry + 1)
						else:
							logging.info('{} crashed, restart attempts timedout.'.format(name))

	def formatPrint(self, name, status, pid, exitcode):
		if status == "RUNNING":
			typeColor = colors.GREEN
		elif status == "EXITED":
			typeColor = colors.BLUE
		elif status == "STOPPED":
			typeColor = colors.YELLOW
		elif status == "NONE":
			typeColor = colors.RESET
		else:
			typeColor = colors.RED
		print("{}{:16} {}{:^16} {}{:^16} {:^16}{}"
		.format(colors.BOLD,name,typeColor,status,colors.WHITE ,pid, exitcode, colors.RESET))

	def isRunning(self):
		print("{}{:16} {:^16} {:^16} {:^16}{}\n".format(colors.BOLD,"Name","Status", "pid", "exitcode", colors.RESET))
		for name in self.prognames:
				if (self.proglist[name] == None):
					self.formatPrint(name, "NONE", 0, "None")
					continue
				for x in range(self.data[name]['numprocs']):
					code = self.proglist[name][x][0].poll()
					pid = self.proglist[name][x][1]
					if (code  == None):
						self.formatPrint(name, "RUNNING", pid, "None")
					elif (code == 0 or code == 2):
						self.formatPrint(name, "EXITED", pid, code)
					elif (code == -9):
						self.formatPrint(name, "STOPPED", pid, code)
					else:
						self.formatPrint(name, "FATAL", pid, code)