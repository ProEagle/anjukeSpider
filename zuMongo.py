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

		select = {"id": zuItem['id']}
		rel = list(db[zone].find(select))
		if len(rel) >= 1:
			return
		db[zone].insert(zuItem)

	def findItem(self, zone, zuSelect):
		conn = MongoClient('localhost', 27017)
		db = conn.anjuke
		rel = list(db[zone].find(zuSelect))
		for i in rel:
			print(i)
		return rel

