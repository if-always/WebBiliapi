# -*-coding:utf-8 -*-
# Date: 2018.6.9
# Author: Jack Cui
# Function: Crawl Bilibili Users infos
# 

import time
import Mysql
import requests
from contextlib import closing

class User:
	"""docstring for """
	def __init__(self,sql):
		
		self.id = Mysql.Select_sql("Bilibili",sql)
		
		self.header_info = {
			'Accept': 'application/json, text/plain, */*',
			'Origin': 'https://space.bilibili.com',
			'Referer': '',
			'Sec-Fetch-Mode': 'cors',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'

		}

		self.header__jp4 = {

			'Referer':'',
			'Sec-Fetch-Mode':'no-cors',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
		}
	

		self.session = requests.session()


	def get_infos(self):

		for _id in self.id:
			_id = _id.get('ownid')
			self.header_info['Referer'] = f'https://space.bilibili.com/{_id}/'
			url = f"https://api.bilibili.com/x/space/acc/info?mid={_id}&jsonp=jsonp"		
			with closing(self.session.get(url, headers=self.header_info, proxies={"http":"http://"+str(requests.get("http://49.235.221.86:5010/get/").json().get('proxy')),"https"+"https://"+str(requests.get("http://49.235.221.86:5010/get/").json().get('proxy'))})) as response:

				if res.get('code') == 0:
					#print(res)
					yield {
						'sex' :res.get('data').get('sex'),
						'name':res.get('data').get('name'),
						'rank':res.get('data').get('rank'),

						
						 }
				break
users = User("""SELECT DISTINCT `ownid` FROM `Videos`""")
a = users.get_infos()

for i in a:
	print(i)