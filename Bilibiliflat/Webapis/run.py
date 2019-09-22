import time
import json
from flask import *
from collections import Counter
from Bilibiliflat.Mysql import *
from Bilibiliflat.Webapis.Predatas import *
app = Flask(__name__)
app.config.from_object(__name__)
predata()


@app.route('/')
def index():

	sql   = """SELECT `tname`,`weeks`,`ctime`,`length`,`owner` FROM `Videos`"""
	datas = Select_sql(dbname="Bilibili",sql=sql)
	tnames = [];ctimes = [];length = [];author = []
	for data in datas:
		tnames.append(data.get('tname'))
		ctimes.append(data.get('ctime'))
		length.append(int(data.get('length')/60))
		author.append(data.get('owner'))

	tnames = Counter(tnames).most_common(20)
	length = Counter(length).most_common()
	author = Counter(author).most_common(500)
	author = [{"name":a[0],"value":a[1]} for a in author]
	length = sorted(length,key=lambda x:x[0])
	

	weeks = [];hours = []
	for ctime in ctimes:
		temp = time.ctime(ctime)
		week = temp.split(' ')[0]
		hour = temp.split(':')[0][-2:]

		if hour == '00':
			hour = '24'
		hour = int(hour)
		hours.append(hour)
		if hour <=6 and hour>=0:
			hour = '凌晨'
		elif hour<=9 and hour>=6:
			hour = '早上'
		elif hour<=12 and hour>=9:
			hour = '上午'
		elif hour<=15 and hour>=12:
			hour = '中午'
		elif hour<=18 and hour>=15:
			hour = '下午'
		elif hour<=21 and hour>=18:
			hour = '晚上'
		else:
			hour = '半夜'
		
		week = week+' :'+hour
		weeks.append(week)
	ctimes = Counter(weeks).most_common()
	chours = Counter(hours).most_common()
	chours = sorted(chours,key=lambda x:x[0])
	infos  = json.dumps({"chours":chours,"ctimes":ctimes,"length":length,"tnames":tnames,"author":author})
	return render_template('index.html',infos=infos)



@app.route('/score')
def score():

	sql = """SELECT `length`,`score`,`tname`,`views`,`coins`,`share`,`likes` FROM Videos"""
	datas = Select_sql(dbname="Bilibili",sql=sql) 
	scores = []
	videos = json.dumps({"videos": datas})
	for data in datas:
		score = round(float(data.get('score')/100000),1)
		scores.append(score)

	scores = Counter(scores).most_common()
	scores = sorted(scores,key=lambda x:x[0])
	scores =json.dumps({'scores':scores})
	categories = ['日常','搞笑','鬼畜调教','单机游戏','美食圈','星海','综合','影视杂谈','综艺','明星','翻唱','影视剪辑','MAD·AMV','电子竞技','美妆']
	return render_template('score.html',scores=scores,videos=videos,categories=categories)


@app.route('/search')
def search():

	sql   = """SELECT * FROM Videos ORDER BY score DESC LIMIT 15"""
	videos = Select_sql(dbname="Bilibili",sql=sql)
	A=[];B=[];
	for video in videos:
		video['ctime'] = time.ctime(video['ctime'])
		video['length']= round(float(video['length']/60),1)

		if video.get('aid') not in A:
			A.append(video.get('aid'))
			B.append(video)
		else:
			for b in B:
				if video.get('aid') == b.get('aid'):
					if video.get('score') > b.get('score'):
					
						new_score = video.get('score')
						
						b['score'] = new_score

		
	videos = B
	return render_template('search.html',videos=videos)


@app.route('/keyword',methods=['POST'])
def keyword():
	data = request.form

	sql = f"""SELECT `aid`,`href`,`title`,`length`,`score`,`owner`,`views`,`likes`,`danmu`,`reply`,`imgurl`,`ctime`,`tname`,`share` FROM Videos AS total WHERE title LIKE '%{data['keyword']}%'"""

	videos = Select_sql(dbname="Bilibili",sql=sql)
	A=[];B=[];
	for video in videos:
		video['ctime'] = time.ctime(video['ctime'])
		video['length']= round(float(video['length']/60),1)

		if video.get('aid') not in A:
			A.append(video.get('aid'))
			B.append(video)
		else:
			for b in B:
				if video.get('aid') == b.get('aid'):
					if video.get('score') > b.get('score'):
					
						new_score = video.get('score')
						
						b['score'] = new_score

		
	videos = B

		
	return json.dumps({"videos": videos})

