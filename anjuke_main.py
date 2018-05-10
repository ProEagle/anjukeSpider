# codeing: utf8
# anjuke_main.py
# 2018.05.06
# 1、解析对应地址的所有房源信息
# 2、并将对应房源信息输出到txt文件中
# 3、将搜索到的信息都存到本地mongo数据库中

from urllib import request
from bs4 import BeautifulSoup
import re
import sys, io, threading
import zuInfo, zuPhone, zuMongo, zuThread

class anjukeSpider(object):
	def __init__(self):
		self.zuData = set()
		self.zuInfo = zuInfo.zuInfo()

	def getInfoFromZone(self, zone):
		self.zuInfo.getRoomItemByZone(zone)

	def getInfoMultiThread(self, zone, threadCount):
		ThreadList = []
		lock = threading.Lock()

		for i in range(0, threadCount):
			t = zuThread.zuThread(zone, 10, lock)
			ThreadList.append(t)
		for t in ThreadList:
			t.start()
		for t in ThreadList:
			t.join()

if __name__ == "__main__":
	zone = 'baoshan'
	objSpider = anjukeSpider()
	# objSpider.getInfoFromZone(zone)
	objSpider.getInfoMultiThread(zone, 5)