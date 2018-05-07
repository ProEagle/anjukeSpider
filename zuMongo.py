#coding: utf-8
# zuMongo.py
# 2018.05.06
# 1、房源的详细信息都存到数据库中

from pymongo import MongoClient
import time, datetime

class zuMongo(object):
	def __init__(self):
		pass

	def contact(self):
		conn = MongoClient('localhost', 27017)
		db = conn.mywebsite
		article = db.articles
		print("连接成功")
		for i in article.find():
			print(i)

	def insertItem(self, zone, zuItem):
		conn = MongoClient('localhost', 27017)
		db = conn.anjuke
		print("连接成功")
		for key in zuItem:
			print(key,": ",zuItem[key])
		db[zone].insert(zuItem)



	def findItem(self):
		pass

