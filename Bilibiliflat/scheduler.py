import time
from Bilibiliflat.api import *
from Bilibiliflat.config import *
from Bilibiliflat.generator import *
from multiprocessing import Process


class Scheduler(object):
    
    @staticmethod
    def spider(cycle=CYCLE):


        while True:
            print('爬虫进程运行')
            #try:
            for website, cls in GENERATOR_MAP.items():
                a = cls + '(website="' + website + '")'
                generator = eval(cls + '(website="' + website + '")')
                generator.run()
                print('爬虫程序结束')
                #generator.close()
                cycle += 1
            if cycle > 21:
                break
            #except Exception as e:
            #    print(e.args)
            #time.sleep(20)
    @staticmethod
    def webapi():
        print('API接口开始运行')
        app.run(host=API_HOST, port=API_PORT)
    
    def run(self):

        if Spider:
            spider_process = Process(target=Scheduler.spider)
            spider_process.start()
            
        
        if Webapi:
            webapi_process = Process(target=Scheduler.webapi)
            webapi_process.start()
            #webapi_process.join()
        
        