
def printhelp():
	with open("help.txt", 'r') as f_help:
		for line in f_help:
			print(line)

def check_command(name, t):
	if ("kill" in name):
		sub = name.split()
		if (len(sub) == 2):
			t.kill(sub[1], out=True)
		elif (len(sub) == 3):
			t.kill(sub[1],pid=int(sub[2]), out=True)
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
	
	if name == "help":
		printhelp()
		return 0

	if name == "clear":
		print("\33[H\33[2J", end="")
		return 0

	if ("reload" in name):
		sub = name.split()
		if (len(sub) == 2):
			responce = input("Are you sure? (y/n) ")
			if (responce == 'y' or responce == 'yes'):
				print("Reloading...")
				t.reloadconf(sub[1])
				print("Done!")
		else:
			print("Syntax Error!\nUsage: start <program>")
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