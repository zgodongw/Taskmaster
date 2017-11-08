from subprocess import *
import sys
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
		self.nameattributes = {} #maybe i'll neeed this later

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
					self.data[name]['stopsignal'] = 'TERM'
				if 'exitcodes' not in self.data[name]:
					self.data[name]['exitcodes'] = [0]
				if 'workingdir' not in self.data[name]:
					self.data[name]['workingdir'] = './'
				if 'umask' not in self.data[name]:
					self.data[name]['umask'] = 000
			except:
				pass

	def run(self):
		self.setKeys()
		for name in self.prognames:
			try:
				outfile = open(self.data[name]['stdout'], "w")
			except:
				outfile = PIPE
			try:
				errorfile = open(self.data[name]['stderr'], "w")
			except:
				errorfile = PIPE
			dictpointer = {}
			try:
				for x in range(self.data[name]['numprocs']):
					string = re.split('\ (?=-)', self.data[name]['cmd'])
					if (self.data[name]['autostart'] == True):
						Pobj = Popen(string, stdout=outfile, stderr=errorfile)
						pid = Pobj.pid
						dictpointer[x] = [Pobj, pid]
					if (dictpointer != {}):
						self.proglist[name] = dictpointer
					else:
						self.proglist[name] = None
			except:
				print("Error couldn't open " + name)
			finally:
				try:
					outfile.close()
					errorfile.close()
				except:
					pass
		
	def	kill(self, string):
		#try:
			for name in self.prognames:
				for x in range(self.data[name]['numprocs']):
					if (string[0] == "all" and (self.proglist[name] != None)):
						kill = self.proglist[name][x][0].kill()
					elif (len(string) > 1):
						if ((name == string[1] or string[1] == "all") and (self.proglist[name] != None)):
							kill = self.proglist[name][x][0].kill()
							print(name + " has been killed!")
		#except:
		#	print(name + " is NOT RUNNING")

	def	stopping(self, string):
		#try:
			for name in self.prognames:
				for x in range(self.data[name]['numprocs']):
					if (string[0] == "all" and (self.proglist[name] != None)):
						kill = self.proglist[name][x][0].terminate()
					elif (len(string) > 1):
						if ((name == string[1] or string[1] == "all") and (self.proglist[name] != None)):
							kill = self.proglist[name][x][0].terminate()
							print(name + " has been stopped!")
		#except:
		#	print(name + " is NOT RUNNING")
	
	def	restarting(self, string):
		for name in self.prognames:
			dictpointer = {}
			try:
				for x in range(self.data[name]['numprocs']):
					if (name == string[1] and self.proglist[name] != None):
						kill = self.proglist[name][x][0].kill()
						tostart = re.split('\ (?=-)', self.data[name]['cmd'])
						Pobj = Popen(tostart)
						pid = Pobj.pid
						dictpointer[x] = [Pobj, pid]
					if (dictpointer != {}):
						self.proglist[name] = dictpointer
			except:
				print("Error couldn't open " + name)


	def	starting(self, string):
		for name in self.prognames:
			try:
				outfile = open(self.data[name]['stdout'], "w")
			except:
				outfile = PIPE
			try:
				errorfile = open(self.data[name]['stderr'], "w")
			except:
				errorfile = PIPE
			dictpointer = {}
			try:
				if ((name == string[1]) and (self.proglist[name] == None)):
					for x in range(self.data[name]['numprocs']):
						if (name == string[1]):
							tostart = re.split('\ (?=-)', self.data[name]['cmd'])
							Pobj = Popen(tostart, stdout=outfile, stderr=errorfile)
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
					print("{:16} {:^16} {:^16} {:^16}".format(name,"!STARTED", 0, "None"))
					continue
				for x in range(self.data[name]['numprocs']):
					status = self.proglist[name][x][0].poll()
					pid = self.proglist[name][x][1]
					if (status  == None):
						print("{:16} {:^16} {:^16} {:^16}".format(name,"RUNNING", pid, "None"))
					elif (status == 0 or status == 2):
						print("{:16} {:^16} {:^16} {:^16}".format(name,"FINISHED", pid, status))
					elif (status == -9):
						print("{:16} {:^16} {:^16} {:^16}".format(name,"STOPPED", pid, status))
					else:
						print("{:16} {:^16} {:^16} {:^16}".format(name,"STOPPED", pid, status))
					
					

	def printit():
		threading.Timer(5.0, printit).start()
		print ("Hello, World!")

class Logger:
	def __init__(self, pathdir):
		self.dirpath = pathdir

	def log(self, msg):
		with open(self.dirpath + "logfile.task", "a+") as logger:
			logger.write(msg)
		logger.close()


def check_command(name, t):
	if ("kill" in name):
		sub = name.split()
		if (len(sub) == 2):
			t.kill(sub)
		else:
			print("Syntax Error!\nUsage: kill <program>")
		return 0

	if ("stop" in name):
		sub = name.split()
		if (len(sub) == 2):
			t.stopping(sub)
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
			t.restarting(sub)
		else:
			print("Syntax Error!\nUsage: restart <program>")
		return 0
	elif ("start" in name):
		sub = name.split()
		if (len(sub) > 1):
			t.starting(sub)
		else:
			print("Syntax Error!\nUsage: start <program>")
		return 0

	if (name == "exit" or name == "quit"):
		t.kill(['all'])
		return -1
	if not name.strip():
		return 12;

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
		t.join()
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
