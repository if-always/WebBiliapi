
def Get_headers(page,arg):

	headers = {
		
		"index":{
		'Host':'www.bilibili.com',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
		'Referer':'https://www.bilibili.com/',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.9',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
				},

		"infos":{
		'Origin':'https://www.bilibili.com',
		'Accept':'*/*',
		'Referer':arg,
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
		
		},
		"author":{
		"Referer": f"https://space.bilibili.com/{arg}?spm_id_from=333.788.b_765f7570696e666f.1",
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
		}
	}

	if page == "index":
		return headers.get("index")
	if page == "infos":
		return headers.get("infos")
	if page == "author":
		return headers.get("author")
