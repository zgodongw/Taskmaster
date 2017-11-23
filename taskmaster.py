from subprocess import *
import sys
import os, signal
import threading
import json
import re


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
					self.data[name]['starttime'] = 1
				if 'stoptime' not in self.data[name]:
					self.data[name][''] = 1
				if 'stopsignal' not in self.data[name]:
					self.data[name]['stopsignal'] = "HUP"
				if 'exitcodes' not in self.data[name]:
					self.data[name]['exitcodes'] = [0]
				if 'workingdir' not in self.data[name]:
					self.data[name]['workingdir'] = './'
				if 'umask' not in self.data[name]:
					self.data[name]['umask'] = 22
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
		raise UnknowSignalError()

	def run(self):
		self.setKeys()
		for prog in self.prognames:
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
	
	def	restarting(self, string):
		self.kill(string)
		self.starting(string, run=True)

	def reloadconf(self, name):
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


	def	starting(self, string, run=False):
		for name in self.prognames:
			try:
				outfile = open(self.data[name]['stdout'], "a+")
			except:
				outfile = PIPE
			try:
				errorfile = open(self.data[name]['stderr'], "a+")
			except:
				errorfile =PIPE 

			wkdir = self.data[name]['workingdir']
			dictpointer = {}
			try:
				if (name == string and (self.proglist[name] == None or run == True)):
					for x in range(self.data[name]['numprocs']):
						if (name == string):			
							tostart = re.split('\ (?=-)', self.data[name]['cmd'])
							Pobj = Popen(tostart, stdout=outfile, stderr=errorfile, cwd=wkdir)
							pid = Pobj.pid
							dictpointer[x] = [Pobj, pid]
						if (dictpointer != {}):
							self.proglist[name] = dictpointer
			except:
				print("Error couldn't open " + name)
			finally:
				try:
					outfile.close()
					errorfile.close()
				except:
					pass
	
	def isRunning(self):
		print("{:16} {:^16} {:^16} {:^16}\n".format("Name","Status", "pid", "exitcode"))
		for name in self.prognames:
				if (self.proglist[name] == None):
					print("{:16} {:^16} {:^16} {:^16}".format(name,"NONE", 0, "None"))
					continue
				for x in range(self.data[name]['numprocs']):
					status = self.proglist[name][x][0].poll()
					pid = self.proglist[name][x][1]
					if (status  == None):
						print("{:16} {:^16} {:^16} {:^16}".format(name,"RUNNING", pid, "None"))
					elif (status == 0 or status == 2):
						print("{:16} {:^16} {:^16} {:^16}".format(name,"EXITED", pid, status))
					elif (status == -9):
						print("{:16} {:^16} {:^16} {:^16}".format(name,"STOPPED", pid, status))
					else:
						print("{:16} {:^16} {:^16} {:^16}".format(name,"FATAL", pid, status))