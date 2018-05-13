#coding: utf-8
# zuInfo.py
# 2018.05.06
# 1、解析房源列表的所有房源信息

from urllib import request
from bs4 import BeautifulSoup
import re, time, logging
import zuPhone, zuMongo, zuLog

class zuInfo(object):
	def __init__(self, loggerName):
		self.zuPhone = zuPhone.zuPhone(loggerName)
		self.mongo = zuMongo.zuMongo()
		self.logger = logging.getLogger(loggerName)
		self.requestErrCnt = 0

	# 根据地区名字拼写，来爬取该地区的房源
	def getRoomItemByZone(self, zone):
		ERROR = -1
		rootUrl = 'https://sh.zu.anjuke.com/fangyuan/'
		url = rootUrl + zone
		zoomItems = []
		for i in range(1, 20):
			if(self.requestErrCnt >= 5):
				self.logger.error(self.getRoomItemByZone.__name__ + ' error')
				self.logger.error('请求出错的次数：' + str(self.requestErrCnt))
				self.logger.error("停止请求url:" +url)
				return ERROR
			self.getRoomItemByPage(zone, url, i)

	# 请求对应地区的对应页面的地址
	def getRoomItemByPage(self, zone, zoneUrl, page):
		ERROR = -1
		url = zoneUrl + '/p'+ str(page)
		zoomItems = self.getParseItem(zone, page, url)
		if zoomItems == ERROR:
			return ERROR
		self.roomItemInFile(zone, zoomItems)
		self.roomItemInMongo(zone, zoomItems)

	# 解析网页，取出每个房源的信息
	def getParseItem(self, zone, page, url):
		ERROR = -1

		try:
			req = request.Request(url)
			req.add_header('user-agent', 'Mozilla/5.0')
			response = request.urlopen(req)
			if (response.getcode() != 200):
				self.logger.error('获取地区搜索详情页失败。')
				self.requestErrCnt += 1
				return ERROR

			htmlStr = response.read()
			soup = BeautifulSoup(htmlStr, 'html.parser', from_encoding='utf-8')

			roomItemColls = []

			zu_floor_req = re.compile(r'\d+/\d+层')
			zu_items = soup.find_all('div', class_='zu-itemmod')
			if len(zu_items) == 0:
				self.requestErrCnt += 1
				self.logger.error(self.getParseItem.__name__ + ' error')
				self.logger.error("解析网页出错，没有解析出房源信息。")
				self.logger.error("当前出错的url:" + url)
				return ERROR
			for item in zu_items: 
				if(self.requestErrCnt >= 5):
					self.logger.error('getparse break')
					self.logger.error('请求出错的次数：' + str(self.requestErrCnt))
					self.logger.error("停止请求url:" +url)
					return ERROR
				zu_item_title = item.find('h3').get_text().lstrip()
				zu_item_info = item.find('p', class_="tag").get_text().lstrip()
				zu_item_info_array = zu_item_info.split('|')
				zu_item_address = item.find('address').get_text().lstrip()
				zu_item_id = item.find('a')['href']
				zu_item_id = re.compile(r'\d+').search(zu_item_id).group()

				zu_item_floor = zu_floor_req.search(zu_item_info_array[2])
				if zu_item_floor == None:
					self.logger.warning("楼层正则解析失败")
					zu_item_floor = ''
				else:
					zu_item_floor = zu_item_floor.group()
				zu_item_landlord = zu_item_info_array[2][len(zu_item_floor)+1:]
				village_a = item.find('a', href=re.compile('view'))
				if (village_a == None) :
					self.logger.warning('小区是空的')
					a_items = item.find_all('a')
					zu_item_village = ''
					for a in a_items:
						self.logger.warning('link: ' + a['href'])
						self.logger.warning('a name: ' + a.get_text())
				else:
					zu_item_village = village_a.get_text().lstrip()

				zu_item_address = zu_item_address[len(zu_item_village):].lstrip()
				zu_item_price = item.find('div', class_="zu-side").get_text().lstrip()

				zu_item_phone = self.zuPhone._get_new_phone(zu_item_id)
				if zu_item_phone == ERROR:
					self.logger.error('获取地区搜索详情页失败。')
					self.requestErrCnt += 1
					continue

				roomItem = {}
				roomItem['title'] = zu_item_title
				roomItem['house_type'] = zu_item_info_array[0]
				roomItem['area'] = zu_item_info_array[1]
				roomItem['floor'] = zu_item_floor
				roomItem['landlord'] = zu_item_landlord
				roomItem['phone'] = zu_item_phone
				roomItem['village'] = zu_item_village
				roomItem['address'] = zu_item_address
				roomItem['rent'] = zu_item_price
				roomItem['id'] = zu_item_id
				roomItem['spier-time'] = int(time.time())
		
				self.logger.info('page：' + str(page))
				self.logger.info('房源id：' + roomItem['id'])			
				self.logger.info('标题：' + roomItem['title'])
				self.logger.info('户型：' + roomItem['house_type'])
				self.logger.info('面积：' + roomItem['area'])
				self.logger.info('楼层：' + roomItem['floor'])
				self.logger.info('房东：' + roomItem['landlord'])	
				self.logger.info('电话：' + roomItem['phone'])	
				self.logger.info('小区：' + roomItem['village'])
				self.logger.info('地址：' + roomItem['address'])
				self.logger.info('租金：' + roomItem['rent'])
				roomItemColls.append(roomItem)

			self.logger.info('每页显示的房源信息数量：' + str(len(roomItemColls)))
			self.logger.info('获取当前地区的详情页面完成。')
			return roomItemColls
		except e:
			self.logger.error(e.message)		
			self.requestErrCnt += 1
			self.logger.error("请求出错的url:"+url)
			self.logger.error("请求"+zone+"地区的第"+page+"页时出现错误")
			self.logger.error("请求已出错的次数:"+self.requestErrCnt)
			return ERROR

	# 将解析出的数据存入mongo数据库
	def roomItemInMongo(self, zone, roomsData):
		if(roomsData == None):
			self.logger.warning("数据为空，不需要写入")
			return
		for roomItem in roomsData:
			self.mongo.insertItem(zone, roomItem)
		self.logger.info("当前页面的内容已写入mongo数据库中")

	# 将解析出的数据写入文件中
	def roomItemInFile(self, zone, roomsData):
		if(roomsData == None):
			self.logger.warning("数据为空，不需要写入")
			return
		timeStr = time.strftime("%Y%m%d", time.localtime(time.time()))
		fileName = 'zuItems_'+zone+'_'+timeStr+'.txt'
		fout = open(fileName, 'w+', encoding='utf8')

		for roomItem in roomsData:
			fout.write('id：' + roomItem['id'] + '\n')			
			fout.write('标题：' + roomItem['title'] + '\n')
			fout.write('户型：' + roomItem['house_type'] + '\n')
			fout.write('面积：' + roomItem['area'] + '\n')
			fout.write('楼层：' + roomItem['floor'] + '\n')
			fout.write('房东：' + roomItem['landlord'] + '\n')	
			fout.write('电话：' + roomItem['phone'] + '\n')	
			fout.write('小区：' + roomItem['village'] + '\n')
			fout.write('地址：' + roomItem['address'] + '\n')
			fout.write('租金：' + roomItem['rent'] + '\n')
		self.logger.info("当前页面的信息已写入" + fileName + "中")
