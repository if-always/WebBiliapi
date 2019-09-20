import time
import requests
from Bilibiliflat.Mysql import *
from Bilibiliflat.loggings import initLogging
from Bilibiliflat.Spiders.bilibili.scores import Biliscores
logger = initLogging("F:/GitHub/Webbiliapi/Loggings/main.log")


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
        
        try:
            args_list = []
            result = self.Get_info(self.args.get('start_url'))
            
            logger.info("数据准备插入到数据库")
            for k,v in result[0].items():
                args_list.append(k)
            Insert_args(db_name=self.args.get('dbname'), table_name=self.args.get('tbname'), data_dict_list=result, arg_list=args_list)
            logger.info("数据库中数据插入完成")

        except Exception as e:
            logger.error(e)

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
        return Biliscores(url).main()
        pass



if __name__ == '__main__':
    b = BilispiderGenerator("Bilibili")
    b.run()