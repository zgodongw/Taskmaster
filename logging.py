class Logger:
	def __init__(self, pathdir):
		self.dirpath = pathdir

	def log(self, msg):
		with open(self.dirpath + "logfile.task", "a+") as logger:
			logger.write(msg)
		logger.close()

	def cout(msg):
		print(msg)