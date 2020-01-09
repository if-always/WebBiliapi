# -*-coding:utf-8 -*-
# Date: 2019.11.19
# Author: Alanda lin
# Function: Crawl Bilibili Users infos
# 

import time
import json
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

		self.header__jp = {

			'Referer':'',
			'Sec-Fetch-Mode':'no-cors',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
		}
		self.session = requests.session()


	def get_infos(self):

		for _id in self.id:
			_id = _id.get('ownid')
			self.header_info['Referer'] = f'https://space.bilibili.com/{_id}/'
			self.header__jp['Referer'] = f'https://space.bilibili.com/{_id}/dynamic'
	
			with closing(self.session.get(url=f"https://api.bilibili.com/x/space/acc/info?mid={_id}&jsonp=jsonp", \
				headers=self.header_info, proxies={"http":"http://"+str(requests.get("http://49.235.221.86:5010/get/")\
					.json().get('proxy'))})) as response:

				if response.json().get('code') == 0:
					_id = _id
					sex = response.json().get('data').get('sex'),
					name = response.json().get('data').get('name'),
					level = response.json().get('data').get('level'),

			with closing(self.session.get(url=f"https://api.bilibili.com/x/space/navnum?mid={_id}&jsonp=jsonp&callback=__jp6", \
				headers=self.header__jp, proxies={"http":"http://"+str(requests.get("http://49.235.221.86:5010/get/")\
					.json().get('proxy'))})) as response:
				response = response.text[6:-1]
				response = json.loads(response)
	
				if response.get('code') ==0:

					video_counts = response.get('data').get('video')
			
						
			with closing(self.session.get(url=f"https://api.bilibili.com/x/relation/stat?vmid={_id}&jsonp=jsonp&callback=__jp4", \
				headers=self.header__jp, proxies={"http":"http://"+str(requests.get("http://49.235.221.86:5010/get/")\
					.json().get('proxy'))})) as response:
				response = response.text[6:-1]
				response = json.loads(response)
	
				if response.get('code') ==0:
					
					follower = response.get('data').get('follower')
					following = response.get('data').get('following')
			with closing(self.session.get(url=f"https://api.bilibili.com/x/space/upstat?mid={_id}&jsonp=jsonp&callback=__jp5", \
				headers=self.header__jp, proxies={"http":"http://"+str(requests.get("http://49.235.221.86:5010/get/")\
					.json().get('proxy'))})) as response:
				response = response.text[6:-1]
				response = json.loads(response)
	
				if response.get('code') ==0:
					
					views = response.get('data').get('archive').get('view')
					likes = response.get('data').get('likes')

			with closing(self.session.get(url=f"https://elec.bilibili.com/api/query.rank.do?mid={_id}&type=jsonp&jsonp=jsonp&callback=__jp10", \
				headers=self.header_info, proxies={"http":"http://"+str(requests.get("http://49.235.221.86:5010/get/")\
					.json().get('proxy'))})) as response:
				response = response.text[7:-1]
				response = json.loads(response)
				
				if response.get('code') ==0:
					coins_counts = response.get('data').get('total_count')
					
				else:
					coins_counts = 0
			
			yield {
						'cid' :_id,
						'sex' :sex[0],
						'nickname' :name[0],
						'views' :views,
						'likes' :likes,
						'level' :level[0],
						'video_counts' :video_counts,
						'coins_counts' :coins_counts,
						'follower' :follower,
						'following' :following,




				}
			break
users = User("""SELECT DISTINCT `ownid` FROM `Videos`""")

a = users.get_infos()
result = list(a)
print(result)
args_list = []
for k,v in result[0].items():
	args_list.append(k)
Mysql.Insert_args(db_name="Bilibili", table_name="Users", data_dict_list=result, arg_list=args_list)
