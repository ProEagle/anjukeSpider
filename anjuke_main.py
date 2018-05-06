# codeing: utf8
# anjuke_main.py
# 20180506
# 主函数，类

from urllib import request
from bs4 import BeautifulSoup
import re
import sys, io
import zuInfo, zuPhone

class anjukeSpider(object):
	def __init__(self):
		self.zuData = set()
		self.zuInfo = zuInfo.zuInfo()


	def getInfoFromZone(self, zone):
		self.zuInfo.getRoomItem(zone)

if __name__ == "__main__":
	zone = 'baoshan'
	objSpider = anjukeSpider()
	objSpider.getInfoFromZone(zone)