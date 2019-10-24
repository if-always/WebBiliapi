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


# A = Select_sql("Bilibili","""SELECT * FROM `Video` WHERE `dates` = '2019-10-16' AND `owner` = '朱一旦的枯燥生活'""")
# print(A)