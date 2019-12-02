import time
import pymysql



def Connect(dbname):

	
		
	db_con = pymysql.connect(host='cdb-hluivpkc.bj.tencentcdb.com',user='root',passwd='byl091022',db=dbname,port=10142,charset='utf8mb4')
	db_cur = db_con.cursor()
	db_cur.execute('SET NAMES utf8mb4')
	db_cur.execute("SET CHARACTER SET utf8mb4")
	db_cur.execute("SET character_set_connection=utf8mb4")
	
	return db_con, db_cur

		




def Select_sql(dbname,sql):

	db_con, db_cur = Connect(dbname)
	data_list = []
	try:
		db_cur.execute(sql)
		desc = db_cur.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
		data_list = [dict(zip([col[0] for col in desc], row)) for row in db_cur.fetchall()]

		#data_list = db_cur.fetchall()
	except Exception:
		return None
	db_con.close()
	return data_list


def Delete_sql(dbname, tbname, user, passwd):

	sql = f"""DELETE FROM {tbname}"""
	db_con, db_cur = Connect(dbname)
	db_cur.execute(sql)
	db_con.commit()
	db_con.close()


def Insert_args(db_name, table_name, data_dict_list, arg_list):
	
	db_con, db_cur = Connect(db_name)
	insertion_part1 = ','.join(arg_list)
	insertion_part2 = ','.join(["%s" for i in range(len(arg_list))])
	insert_clause = '''INSERT INTO %s (%s) VALUES (%s)''' % (table_name, insertion_part1, insertion_part2)
	

	insert_param = []
	for data_dict in data_dict_list:
		insert_param.append(tuple((data_dict.get(arg) for arg in arg_list)))
	insert_param_set = set(insert_param)  # set去重
	insert_param = list(insert_param_set)

	try:
		
		db_cur.executemany(insert_clause,insert_param)
		db_con.commit()
		print("插入完成")

	except Exception as e:
		print(e)
		db_con.rollback()
		db_con.close()