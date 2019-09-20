import time
import pymysql
from Bilibiliflat.config import *
from Bilibiliflat.loggings import initLogging
logger = initLogging("sql.log")


def Connect(dbname):

	
		
	db_con = pymysql.connect(host='cdb-hluivpkc.bj.tencentcdb.com',user=user,passwd=passwd,db=dbname,port=10142,charset='utf8mb4')
	db_cur = db_con.cursor()
	db_cur.execute('SET NAMES utf8mb4')
	db_cur.execute("SET CHARACTER SET utf8mb4")
	db_cur.execute("SET character_set_connection=utf8mb4")
	
	return db_con, db_cur

		


def insert_by_args(db_name, table_name, user,passwd,data_dict_list, arg_list):
	
	db_con, db_cur = connect(db_name,user,passwd)
	insertion_part1 = ','.join(arg_list)
	insertion_part2 = ','.join(["%s" for i in range(len(arg_list))])
	insert_clause = '''INSERT INTO %s (%s) VALUES (%s)''' % (table_name, insertion_part1, insertion_part2)
	logger.debug(insert_clause)

	insert_param = []
	for data_dict in data_dict_list:
		insert_param.append(tuple((data_dict.get(arg) for arg in arg_list)))
	insert_param_set = set(insert_param)  # set去重
	insert_param = list(insert_param_set)

	try:
		print(insert_clause)
		print('正在插入数据...')
		print(insert_param)
		db_cur.executemany(insert_clause,insert_param)
		db_con.commit()
		print("插入完成")
	except Exception as e:
		logger.error(e)
		logger.error('批量插入失败，进行数据插入回滚')
		db_con.rollback()
		db_con.close()


def Select_sql(dbname,sql):

	db_con, db_cur = Connect(dbname)
	data_list = []
	try:
		db_cur.execute(sql)
		desc = db_cur.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
		data_list = [dict(zip([col[0] for col in desc], row)) for row in db_cur.fetchall()]

		#data_list = db_cur.fetchall()
	except Exception:
		logger.error("获取数据出错")
	db_con.close()
	return data_list

# b = "Bilibili"
# a = Select_sql("Args",f"""SELECT * FROM `spiders`WHERE `names` = '{b}'""")

# print(a)
# def A(num):
# 	print ('Process:', num)
# 	time.sleep(10)
# def B(num):
# 	print ('Process:', num)
# 	time.sleep(1)

# if __name__ == '__main__':
#     if True:
#         p = multiprocessing.Process(target=A, args=(1,))
#         p.start()
#     if True:
#     	q = multiprocessing.Process(target=B, args=(2,))
#     	q.start()