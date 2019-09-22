from Bilibiliflat.Mysql import *


def predata():

	sql = "SELECT * FROM Video AS a WHERE `times` LIKE '%22:2%'"
	datas = Select_sql(dbname="Bilibili", sql=sql)

	Delete_sql(dbname="Bilibili",tbname="Videos",user="root",passwd="byl091022")

	args_list = []
	
	for k,v in datas[0].items():
		args_list.append(k)
		

	Insert_args(db_name="Bilibili", table_name="Videos", data_dict_list=datas, arg_list=args_list)
