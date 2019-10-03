from Bilibiliflat.Mysql import *


def predata():

<<<<<<< HEAD
	sql = "SELECT * FROM Video WHERE `times` LIKE '%22:2%'"
=======
	sql = "SELECT * FROM Video AS a WHERE `times` LIKE '%22:2%'"
>>>>>>> alanda
	datas = Select_sql(dbname="Bilibili", sql=sql)

	Delete_sql(dbname="Bilibili",tbname="Videos",user="root",passwd="byl091022")

	args_list = []
	
	for k,v in datas[0].items():
		args_list.append(k)
		

	Insert_args(db_name="Bilibili", table_name="Videos", data_dict_list=datas, arg_list=args_list)
