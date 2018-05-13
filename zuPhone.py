#coding: utf-8
# zuPhone.py
# 2018.05.06
# 1、解析房东的电话号码

from urllib import request
from bs4 import BeautifulSoup
import http.cookiejar
import re, logging

class zuPhone(object):

	def __init__(self, loggerName):
		self.logger = logging.getLogger(loggerName)

	# 获取联系人的电话
	def _get_new_phone(self, zuId):
		ERROR = -1

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
			self.logger.error('请求房源详情页失败')
			return ERROR

		phone = self._get_require_args(response.read(), zuId, url)
		return phone
		# self._get_phone_json(args)

	def _get_require_args(self, html, zuId, url):
		ERROR = -1

		soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
		jsObjects = soup.find_all('script')
		jsCont = ''
		for one in jsObjects:
			jsCont = jsCont + one.get_text()
		argsReq = re.compile(r'ajk\.page\.Zufang.*?;', re.DOTALL)
		argstr = argsReq.search(jsCont);
		if argstr == None:
			self.logger.error('房源'+str(zuId) + '解析参数失败')
			self.logger.error("电话解析不出来的url:", url)
			self.logger.error(jsCont)
			return ERROR
		argstr = argstr.group()
		retArgs = {}
		retArgs['broker_id'] = re.compile(r'broker_id:\'(\d*)\'', re.DOTALL).search(argstr).group(1)
		retArgs['city_id'] = re.compile(r'city_id:\'(\d*)\'', re.DOTALL).search(argstr).group(1)
		retArgs['prop_id'] = re.compile(r'prop_id:\'(\d*)\'', re.DOTALL).search(argstr).group(1)
		retArgs['broker_phone'] = re.compile(r'brokerPhone:\'(\d*)\'', re.DOTALL).search(argstr).group(1)
		retArgs['token'] = re.compile(r'token: (\'.*?\')', re.DOTALL).search(argstr).group(1)
		retArgs['token'] = retArgs['token'].split('\'')[1]

		return retArgs['broker_phone']

	def _get_phone_json(self, retarg):
		ERROR = -1

		urlReqPhone = 'https://sh.zu.anjuke.com/v3/ajax/getBrokerPhone/?'
		url = urlReqPhone + 'broker_id=' + retarg['broker_id']
		url = url + '&token=' + retarg['token']
		url = url + '&prop_id=' + retarg['prop_id']
		url = url + '&prop_city_id=' + retarg['city_id']
		self.logger.info('请求房东电话json的url：'+ url)

		req = request.Request(url)
		req.add_header('user-agent', 'Mozilla/5.0')
		response = request.urlopen(req)

		if response.getcode() != 200 :
			self.logger.error('请求房东json数据失败')
			return ERROR
		self.info(response.read())
		






