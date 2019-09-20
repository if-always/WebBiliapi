import time
import datetime
import requests
from Bilibiliflat.loggings import initLogging
from Bilibiliflat.Spiders.bilibili.Header import Get_headers
from pyquery import PyQuery as pq

class Biliscores(object):
	"""docstring for Biliscores"""
	def __init__(self, arg):
		super(Biliscores, self).__init__()
		self.url = arg
		self.logger = initLogging("Loggings/spider.log")
	def Get_resqs(self,url,headers):
		
		res = requests.get(url=url,headers=headers)

		if res.status_code == 200:
			return res

		else:
			return None


	def Get_index(self):
		
		html = self.Get_resqs(self.url,Get_headers("index",None))
		
		doc = pq(html.text)

		infos = doc("ul.rank-list").find("li.rank-item").items()


		for info in infos:
			#print(info)
			try:
				rank = info.find("div.num").text()
				href = "https:"+info.find("div.content div.img a").attr("href")
				
				title = info.find("div.content div.info a").text()
				score = info.find("div.content div.info div.pts div").text()
				#print(score)
				if href == "https://www.bilibili.com/video/av63276042/":
					continue
				args = self.Get_infos(href)
				#print(title)
				self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
				print(self.time + "  " + title)
				dates = datetime.datetime.now().date()
				times = datetime.datetime.now().time()
				weeks = datetime.datetime.now().ctime().split(" ")[0]

				yield {
						'aid'  :args[0],
						'cid'  :args[1],
						'href' :href,
						'rank' :rank,
						'dates':dates,
						'times':times,
						'weeks':weeks,
						'score':score,
						'title':title,
						'tname':args[2],
						'owner':args[3],
						'ownid':args[4],
						'owurl':args[5],
						'views':args[6],
						'danmu':args[7],
						'reply':args[8],
						'favou':args[9],
						'coins':args[10],
						'share':args[11],
						'likes':args[12],
						'ctime':args[13],
						'length':args[14],
						'imgurl':args[15],


				}
				self.logger.info(str(rank) + ':'+str(title))
			except Exception as e:
				print(e)
				self.logger.error(title + " " +str(e))
			time.sleep(0.5)
			#break
	def Get_infos(self,href):
		
		aid = href.split("/")[-2][2:]
		temp = self.Get_resqs(f"https://api.bilibili.com/x/web-interface/view?aid={aid}",Get_headers("infos",href)).json()
		#print(href)
		#print(f"https://api.bilibili.com/x/web-interface/view?aid={aid}")
		info = temp.get("data")
		#print(info)
		cid  = info.get('cid')
		tname= info.get('tname')
		owner= info.get('owner').get('name')
		owaid= info.get('owner').get('mid')
		owurl= "https://space.bilibili.com/"+str(owaid)
		views= info.get('stat').get('view')
		danmu= info.get('stat').get('danmaku')
		reply= info.get('stat').get('reply')
		favou= info.get('stat').get('favorite')
		coins= info.get('stat').get('coin')
		share= info.get('stat').get('share')
		likes= info.get('stat').get('like')
		ctime= info.get('ctime')
		length = info.get('duration')
		imgurl = info.get('pic')
		return (aid,cid,tname,owner,owaid,owurl,views,danmu,reply,favou,coins,share,likes,ctime,length,imgurl) 
	

	def main(self):
		a = self.Get_index()
		return list(a)