# codeing: utf8
# anjuke_main.py
# 2018.05.06
# 1、解析对应地址的所有房源信息
# 2、并将对应房源信息输出到txt文件中
# 3、将搜索到的信息都存到本地mongo数据库中

import threading, time, sys, io
import zuInfo, zuPhone, zuMongo, zuThread, zuLog

class anjukeSpider(object):
	def __init__(self):
		self.loggerName = 'debugLogger'
		self.logFileName = './log/' + time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time())) + '.log'

		self.zuInfo = zuInfo.zuInfo(self.loggerName)
		self.log = zuLog.zuLogging(self.loggerName)

		self.page = 10
		self.loaddingPage = 1

	def getInfoFromZone(self, zone):
		self.zuInfo.getRoomItemByZone(zone)

	def getInfoMultiThread(self, zone, threadCount):
		ThreadList = []
		lock = threading.Lock()

		for i in range(0, threadCount):
			t = zuThread.zuThread(zone, 10, lock, self)
			ThreadList.append(t)
		for t in ThreadList:
			t.start()
		for t in ThreadList:
			t.join()

if __name__ == "__main__":

	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

	zone = 'baoshan'
	# timeStr = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
	# logFileName = timeStr+'.log'

	objSpider = anjukeSpider()
	# objSpider.getInfoFromZone(zone)
	objSpider.log.config("DEBUG", "DEBUG", objSpider.logFileName)
	objSpider.getInfoMultiThread(zone, 5)