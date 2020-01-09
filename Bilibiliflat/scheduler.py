import time
from Bilibiliflat.Webapis.run import *
from Bilibiliflat.config import *
from Bilibiliflat.generator import *
from multiprocessing import Process
from Bilibiliflat.loggings import initLogging
logger = initLogging("C:\\Users\\17121\\OneDrive\\Githubproject\\Crawlitems\\WebBiliapi\\Loggings\\main.log")

class Scheduler(object):
    
    @staticmethod
    def spider(cycle=CYCLE):


        #while True:
        
        try:
            logger.info('爬虫模块正在运行')
            for website, cls in GENERATOR_MAP.items():
                a = cls + '(website="' + website + '")'
                generator = eval(cls + '(website="' + website + '")')
                generator.run()
            logger.info('爬虫模块结束运行')
                
        except Exception as e:
           logger.error(e)
        
    @staticmethod
    def webapi():
        logger.info('API接口开始运行')
        app.run(debug=True)
    
    def run(self):

        if Spider:
            spider_process = Process(target=Scheduler.spider)
            spider_process.start()
            
        
        if Webapi:
            webapi_process = Process(target=Scheduler.webapi)
            webapi_process.start()
            #webapi_process.join()
        
        