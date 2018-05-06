#coding: utf-8

from urllib import request
from bs4 import BeautifulSoup
import http.cookiejar
import re
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
url = 'https://sh.zu.anjuke.com/fangyuan/baoshan/'

class zuPhone(object):

	# 获取联系人的电话
	def _get_new_phone(self, zuId):
		urlFront = 'https://sh.zu.anjuke.com/fangyuan/'
		url = urlFront + zuId
		cj = http.cookiejar.CookieJar()
		cookie = request.HTTPCookieProcessor(cj)
		opener = request.build_opener(cookie)
		request.install_opener(opener)

		req = request.Request(url)
		req.add_header('user-agent', 'Mozilla/5.0')
		response = request.urlopen(req)

		if response.getcode() != 200 :
			print('请求房源详情页失败')
			return

		phone = self._get_require_args(response.read())
		return phone
		# self._get_phone_json(args)

	def _get_require_args(self, html):
		soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
		jsObjects = soup.find_all('script')
		jsCont = ''
		for one in jsObjects:
			jsCont = jsCont + one.get_text()
		argsReq = re.compile(r'ajk\.page\.Zufang.*?;', re.DOTALL)
		argstr = argsReq.search(jsCont);
		if argstr == None:
			print('解析参数失败')
			return
		argstr = argstr.group()
		# print("对应参数" + argstr)
		retArgs = {}
		retArgs['broker_id'] = re.compile(r'broker_id:\'(\d*)\'', re.DOTALL).search(argstr).group(1)
		retArgs['city_id'] = re.compile(r'city_id:\'(\d*)\'', re.DOTALL).search(argstr).group(1)
		retArgs['prop_id'] = re.compile(r'prop_id:\'(\d*)\'', re.DOTALL).search(argstr).group(1)
		retArgs['broker_phone'] = re.compile(r'brokerPhone:\'(\d*)\'', re.DOTALL).search(argstr).group(1)
		retArgs['token'] = re.compile(r'token: (\'.*?\')', re.DOTALL).search(argstr).group(1)
		retArgs['token'] = retArgs['token'].split('\'')[1]
		# 获取房东id，城市id，房东电话，网页token， 属性id
		# print('broker_id', retArgs['broker_id'])
		# print('city_id', retArgs['city_id'])
		# print('prop_id', retArgs['prop_id'])
		# print('broker_phone', retArgs['broker_phone'])
		# print('token', retArgs['token'])

		return retArgs['broker_phone']

	def _get_phone_json(self, retarg):

		urlReqPhone = 'https://sh.zu.anjuke.com/v3/ajax/getBrokerPhone/?'
		url = urlReqPhone + 'broker_id=' + retarg['broker_id']
		url = url + '&token=' + retarg['token']
		url = url + '&prop_id=' + retarg['prop_id']
		url = url + '&prop_city_id=' + retarg['city_id']
		print('请求房东电话json的url：'+ url)

		req = request.Request(url)
		req.add_header('user-agent', 'Mozilla/5.0')
		response = request.urlopen(req)

		if response.getcode() != 200 :
			print('请求房东json数据失败')
			return
		print(response.read())
		


if __name__ == '__main__':
	zuId = '1149876158'
	obj_zuPhone = zuPhone()
	obj_zuPhone._get_new_phone(zuId)







