#coding: utf-8
# zuThread.py
# 2018.05.09
# 使用多线程来爬数据

import threading
import time, random, logging
import zuInfo

class zuThread(threading.Thread):

	def __init__(self, zone, maxPage, lock):
		threading.Thread.__init__(self)
		self.zuInfo = zuInfo.zuInfo()
		self.lock = lock
		self.maxPage = maxPage
		self.zone = zone
		self.loaddingPage = 1;

	def run(self):
		rootUrl = 'https://sh.zu.anjuke.com/fangyuan/'
		url = rootUrl + self.zone
		print("threading name:", self.name)
		# print("threading id:", self.id)
		if self.loaddingPage > self.maxPage:
			print("全部页面都正在下载中...")
			return
		while self.loaddingPage <= self.maxPage:
			if self.lock.acquire():
				if self.loaddingPage <= self.maxPage:
					pageIndex = self.loaddingPage
					self.loaddingPage += 1
					self.lock.release()
					self.zuInfo.getRoomItemByPage(self.zone, url, pageIndex)
				else:
					self.lock.release();
					return


		# nothingToRun(n, self)

		# global n, lock, upLimit
		# time.sleep(1)
		# if(n >= upLimit):
		# 	print("get number", n)
		# 	print("整个线程结束")
		# 	return
		# if lock.acquire():
		# 	nothingToRun(n, self)
		# 	n += 1
		# 	lock.release()

# def nothingToRun(a, b):
# 	aInt = 0
# 	global n, upLimit
# 	if n >= upLimit:
# 		return
# 	while aInt <= upLimit and n <= upLimit:
# 		ns = random.randint(0, 2)
# 		print("thread name: ", b.name)
# 		print("延时" + str(ns) + "秒")
# 		time.sleep(ns)
# 		if lock.acquire():
# 			if n <= upLimit:
# 				aInt = n
# 				n += 1
# 				print("锁中 get number: aInt = ", aInt)
# 				print("锁中 get number: n = ", n)
# 				print("锁中 thread name: ", b.name)
# 			lock.release()
# 	print(b.name, "最终结束时number:", aInt)

# if "__main__" == __name__:
# 	logger = logging.getLogger()
# 	logger.setLevel(logging.INFO)
# 	date = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))
# 	log_name = date + '.log'
# 	fn = logging.FileHandler(log_name, mode='w')
# 	fn.setLevel(logging.DEBUG)
# 	# formatter = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
# 	# fn.setFormatter(formatter)
# 	logger.addHandler(fn)

# 	# loggin.basicConfig(level=logging.DEBUG, 
# 	# 					format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# 	n = 1
# 	upLimit = 100
# 	ThreadList = []
# 	logger.debug('main start')
# 	lock = threading.Lock()
# 	for i in range(0, 30):
# 		t = zuThread()
# 		ThreadList.append(t)
# 	for t in ThreadList:
# 		t.start()
# 	for t in ThreadList:
# 		t.join()
# 	logger.debug("n = "+ str(n))
# 	logger.debug('this is a loger debug')