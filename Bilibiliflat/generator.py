import time
import requests
from Bilibiliflat.Mysql import *
from Bilibiliflat.Spiders.bilibili.scores import Biliscores

class SpiderGenerator(object):

    def __init__(self, website='default'):
        
        """
        父类, 初始化一些对象
        """
        self.args = Select_sql("Args",f"""SELECT * FROM `spiders` WHERE `names` = '{website}'""")[0]

        

    def Get_info(self):
        """
        功能由子类重写
        """
        raise NotImplementedError

    
    def run(self):
        

        
        result = self.Get_info(self.args.get('start_url'))

    
    


class BilispiderGenerator(SpiderGenerator):
    def __init__(self, website='Bilibili'):
        """
        初始化操作
        :param website: 站点名称
        :param browser: 使用的浏览器
        """
        SpiderGenerator.__init__(self, website)
        self.website = website
        
    def Get_info(self,url):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        print(url)
        return Biliscores(url).main()
        pass



if __name__ == '__main__':
    b = BilispiderGenerator("Bilibili")
    b.run()