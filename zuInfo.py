#coding: utf-8
# zuInfo.py
# 2018.05.06
# 1、解析房源列表的所有房源信息

from urllib import request
from bs4 import BeautifulSoup
import re
import sys, io, time, datetime
import zuPhone, zuMongo, zuThread

class zuInfo(object):
	def __init__(self):
		self.zuPhone = zuPhone.zuPhone()
		self.mongo = zuMongo.zuMongo()
		self.requestErrCnt = 0


	def getRoomItemByZone(self, zone):
		rootUrl = 'https://sh.zu.anjuke.com/fangyuan/'
		url = rootUrl + zone
		zoomItems = []
		for i in range(1, 20):
			if(self.requestErrCnt >= 5):
				print("停止请求url:" +url)
				return
			self.getRoomItemByPage(zone, url, i)


	def getRoomItemByPage(self, zone, zoneUrl, page):
		url = zoneUrl + '/p'+ str(page)
		zoomItems = self.getParseItem(zone, page, url)
		self.roomItemInFile(zone, zoomItems)
		self.roomItemInMongo(zone, zoomItems)

	def getParseItem(self, zone, page, url):
		
		try:
			req = request.Request(url)
			req.add_header('user-agent', 'Mozilla/5.0')
			response = request.urlopen(req)
			if (response.getcode() != 200):
				print('获取地区搜索详情页失败。')
				self.requestErrCnt += 1
				return None

			htmlStr = response.read()
			soup = BeautifulSoup(htmlStr, 'html.parser', from_encoding='utf-8')

			roomItemColls = []

			zu_floor_req = re.compile(r'\d+/\d+层')
			zu_items = soup.find_all('div', class_='zu-itemmod')
			for item in zu_items: 
				zu_item_title = item.find('h3').get_text().lstrip()
				zu_item_info = item.find('p', class_="tag").get_text().lstrip()
				zu_item_info_array = zu_item_info.split('|')
				zu_item_address = item.find('address').get_text().lstrip()
				zu_item_id = item.find('a')['href']
				zu_item_id = re.compile(r'\d+').search(zu_item_id).group()

				zu_item_floor = zu_floor_req.search(zu_item_info_array[2])
				if zu_item_floor == None:
					print("楼层正则解析失败")
					zu_item_floor = ''
				else:
					zu_item_floor = zu_item_floor.group()
				zu_item_landlord = zu_item_info_array[2][len(zu_item_floor)+1:]
				village_a = item.find('a', href=re.compile('view'))
				if (village_a == None) :
					print('小区是空的')
					a_items = item.find_all('a')
					zu_item_village = ''
					for a in a_items:
						print('link: ' + a['href'])
						print('a name: ' + a.get_text())

				else:
					zu_item_village = village_a.get_text().lstrip()

				zu_item_address = zu_item_address[len(zu_item_village):].lstrip()
				zu_item_price = item.find('div', class_="zu-side").get_text().lstrip()

				zu_item_phone = self.zuPhone._get_new_phone(zu_item_id)

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
		
				print('page：' + str(page))
				print('房源id：' + zu_item_id)
				print('标题：' + zu_item_title)
				print('详情：' + zu_item_info)
				print("楼层：" + zu_item_floor)
				print('地址：' + zu_item_address)
				print('租金：' + zu_item_price)
				print('房东：' + zu_item_landlord)
				print('电话：' + zu_item_phone)
				roomItemColls.append(roomItem)
			print('每页显示的房源信息数量：', len(roomItemColls))
			print('获取当前地区的详情页面完成。')
			return roomItemColls
		except e:
			print(e.message)		
			self.requestErrCnt += 1
			print("请求出错的url:"+url)
			print("请求"+zone+"地区的第"+page+"页时出现错误")
			print("请求已出错的次数:"+self.requestErrCnt)
			return None


	def roomItemInMongo(self, zone, roomsData):
		if(roomsData == None):
			print("数据为空，不需要写入")
			return
		for roomItem in roomsData:
			self.mongo.insertItem(zone, roomItem)
		print("当前页面的内容已写入mongo数据库中")

	def roomItemInFile(self, zone, roomsData):
		if(roomsData == None):
			print("数据为空，不需要写入")
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
		print("当前页面的信息已写入" + fileName + "中")
