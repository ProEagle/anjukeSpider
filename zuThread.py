#coding: utf-8
# zuThread.py
# 2018.05.09
# 使用多线程来爬数据

import threading
import time, random, logging
import zuInfo

class zuThread(threading.Thread):

	def __init__(self, zone, maxPage, lock, anjuke):
		threading.Thread.__init__(self)
		self.logger = logging.getLogger(anjuke.loggerName)
		self.zuInfo = anjuke.zuInfo
		self.lock = lock
		self.maxPage = maxPage
		self.zone = zone
		self.anjuke = anjuke

	# 线程启动,线程的主函数，主要用于取地区搜索结果的不同页面
	def run(self):
		rootUrl = 'https://sh.zu.anjuke.com/fangyuan/'
		url = rootUrl + self.zone
		self.logger.info("threading name:" + self.name)
		# print("threading id:", self.id)
		if self.anjuke.loaddingPage > self.maxPage:
			self.logger.warning("全部页面都正在下载中...")
			return
		while self.anjuke.loaddingPage <= self.maxPage:
			if self.lock.acquire():
				if self.anjuke.loaddingPage <= self.maxPage:
					if self.anjuke.zuInfo.requestErrCnt >= 5:
						self.logger.error(self.run.__name__ + ' error')
						self.logger.error('请求出错的次数：' + str(self.anjuke.zuInfo.requestErrCnt))
						self.logger.error(self.name + '退出')
						self.lock.release()
						return
					pageIndex = self.anjuke.loaddingPage
					self.anjuke.loaddingPage += 1
					self.lock.release()
					self.zuInfo.getRoomItemByPage(self.zone, url, pageIndex)
				else:
					self.logger.warning("全部页面已经都正在下载中...")
					self.lock.release();
					return
