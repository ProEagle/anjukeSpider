#coding: utf-8
# zuInfo.py
# 2018.05.06
# 1、解析房源列表的所有房源信息

from urllib import request
from bs4 import BeautifulSoup
import re
import sys, io
import zuPhone

class zuInfo(object):
	def __init__(self):
		self.zuPhone = zuPhone.zuPhone()

	def getRoomItem(self, zone):
		rootUrl = 'https://sh.zu.anjuke.com/fangyuan/'
		url = rootUrl + zone

		req = request.Request(url)
		req.add_header('user-agent', 'Mozilla/5.0')
		response = request.urlopen(req)
		if (response.getcode() != 200):
			print('获取地区搜索详情页失败。')
			return
		htmlStr = response.read()
		soup = BeautifulSoup(htmlStr, 'html.parser', from_encoding='utf-8')

		fout = open('zu.txt', 'w', encoding='utf8')
		zu_floor_req = re.compile(r'\d+/\d+层')
		print('搜索到的房源地址')
		zu_items = soup.find_all('div', class_='zu-itemmod')
		for item in zu_items: 
			fout.write('租房房源：\n')
			zu_item_title = item.find('h3').get_text().lstrip()
			zu_item_info = item.find('p', class_="tag").get_text().lstrip()
			zu_item_info_array = zu_item_info.split('|')
			zu_item_address = item.find('address').get_text().lstrip()
			zu_item_id = item.find('a')['href']
			zu_item_id = re.compile(r'\d+').search(zu_item_id).group()
			print('房源id：' + zu_item_id)

			zu_item_floor = zu_floor_req.search(zu_item_info_array[2])
			if zu_item_floor == None:
				print("楼层正则解析失败")
			else:
				zu_item_floor = zu_item_floor.group()
				print("楼层：" + zu_item_floor)
			zu_item_landlord = zu_item_info_array[2][len(zu_item_floor)+1:]
			print('房东：' + zu_item_landlord)
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

			print('标题：' + zu_item_title)
			print('详情：' + zu_item_info)
			print('地址：' + zu_item_address)
			print('租金：' + zu_item_price)
			zu_item_phone = self.zuPhone._get_new_phone(zu_item_id)
			print('电话：' + zu_item_phone)

			fout.write('标题：' + zu_item_title + '\n')
			fout.write('户型：' + zu_item_info_array[0] + '\n')
			fout.write('面积：' + zu_item_info_array[1] + '\n')
			fout.write('楼层：' + zu_item_floor + '\n')
			fout.write('房东：' + zu_item_landlord + '\n')	
			fout.write('电话：' + zu_item_phone + '\n')	
			fout.write('小区：' + zu_item_village + '\n')
			fout.write('地址：' + zu_item_address + '\n')
			fout.write('租金：' + zu_item_price + '\n')


		print('获取当前地区的详情页面完成。')

