#coding: utf-8
# zuLog.py
# 2018.05.12
# 封装输出log的类

import time, logging

class zuLogging(object):
	def __init__(self, loggerName):
		self.logger = logging.getLogger(loggerName)
		pass

	def config(self, fileLevelFlag, cmdLevelFlag, logFileName):
		levelsDic = {
			"DEBUG":logging.DEBUG,
			"INFO":logging.INFO,
			"WARN": logging.WARN,
			"ERROR": logging.ERROR
			}
		self.logger.setLevel(levelsDic[fileLevelFlag])

		# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s','%H:%M:%S')

		fileHandle = logging.FileHandler(logFileName, 'w', 'utf-8')
		fileHandle.setLevel(levelsDic[fileLevelFlag])
		fileHandle.setFormatter(formatter)

		cmdHandle = logging.StreamHandler()
		cmdHandle.setLevel(levelsDic[cmdLevelFlag])
		cmdHandle.setFormatter(formatter)
		
		self.logger.addHandler(fileHandle)
		self.logger.addHandler(cmdHandle)

# if "__main__" == __name__:
# 	obj = zuLogging('debug_log', 'simLog.log')
# 	obj.config("DEBUG", 'sing.log')
# 	obj.log("DEBUG", "debug message")
# 	obj.log("INFO", "info message")
# 	obj.log("WARN", "warn message")
# 	obj.log("ERROR", "error message")


