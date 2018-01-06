import smtplib
import getpass

def getGodPassword():
	print("Warning: The God privelege is only for those who truly\nunderstand the taskmaster!\n")

	passwd = getpass.getpass('Please enter God Password: ')
	if passwd == 'turtledove':
		return 1
	print("Error: Incorrect password! : God Privelege denied!\nLogging in as human...")
	return 0

def getUser(optargs):
	if optargs:
		var = int()
		if optargs == 'God':
			var = getGodPassword()
			if var == 1:
				return 'God'
		return 'human'
	return 'human'

def sendLogReport(toaddr):
	print("Please wait we send a log report...")
    
	fromaddr = 'taskmaster.logreport@gmail.com'

	with open("Taskmaster.log", 'r') as task:
		string = task.read()
	try:
		msg = "Subject: {}\n\n{}".format("Log Report", "TASKMASTER LOG REPORT\n\n\n" + string)
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, 'turtledove')
		server.sendmail(fromaddr, toaddr, msg)
		server.quit()
	except:
		print("Error occured while try to send a log report! Please check email address")
