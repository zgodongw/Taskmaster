import smtplib

def getGodPassword():
	print("Warning: The God privelege is only for those who truly\nunderstand the taskmaster!\n")

	passwd = input('Please enter God Password: ')
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
		else:
			return 'human'
	else:
		return 'human'

def sendLogReport(toaddress):
    pass