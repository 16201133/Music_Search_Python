import pymysql
import configparser

def read_config():
    # 读取配置文件
    cf = configparser.ConfigParser()
    cf.read('D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/语音识别/db.ini')
    # 获取配置文件中 所有的section(一个配置文件中可以有多个配置,如Mysql、sqlserver、oracle等)
    # secs = cf.sections()
    # print("配置文件:",secs)
    host = cf.get('Mysql-Database', 'host')
    username = cf.get('Mysql-Database', 'username')
    password = cf.get('Mysql-Database', 'password')
    database = cf.get('Mysql-Database', 'database')
    port = cf.get('Mysql-Database', 'port')
    port = int(port)
    charset = cf.get('Mysql-Database', 'charset')
    data = [host,username,password,database,port,charset]

    return data

class DBUtil:

    def __init__(self, data):
        data = read_config()
        self.host = data[0]
        self.username = data[1]
        self.password = data[2]
        self.database = data[3]
        self.port = data[4]
        self.charset = data[5]
    def getconn(self):
        """
        连接数据库
        :return: db
        """
        self.db = pymysql.connect(host=self.host,user=self.username,password=self.password,database=self.database,port=self.port,charset=self.charset)

    def get_cursor(self):
        """获取游标"""
        self.cursor = self.db.cursor()
        return self.cursor

    def close_db(self):
        """关闭连接"""
        self.cursor.close()
        self.db.close()

    # 查询语句(所有结果集) ————————简洁版
    def QueryMany_Concise(self, sql):
        results = ''
        # 1、获得连接
        self.getconn()

        # 2、创建游标
        cursor = self.get_cursor()

        try:
            # 3、执行SQL语句
            rows = cursor.execute(sql)
            # 4、获取所有记录列表
            if rows > 0:
                results = cursor.fetchall()
            else:
                results = ''
        except:
            print("查询语句异常")
        # 5、关闭连接
        self.close_db()
        return results
    # 查询语句(所有结果集) ————————不太好,太繁杂
    def QueryMany(self, tablename, claim='', orders='', fields='*'):
        """
        查询功能
                SQL： select id,song_name,song_address from songs where song_name='年少有为' order by id(ASC)
        调用方式：
                claim = {'song_name':'年少有为','song_singer':'李荣浩'}
                orders = [{'song_id':'ASC'},{'song_name':'DESC'}]
                fields = ['song_id','song_address']
                db.QueryMany(tablename="songs",claim=claim,orders=orders,fields=fields)
        参数详情：
                :param tablename: 表名
                :param claim: 查询条件（字典类型）
                :param orders: 排序条件（列表-字典类型——支持多条件查询） eg. orders = [{'age':'18'},{'age1':'19'}]
                :param fields: 想要的信息（列表类型）                  eg. id,name,sex等信息
                :return: 查询结果集
        """
        # 1、获得SQL语句
        # 表名 and 表属性信息（id,name,sex等信息）
        sql = ''
        if fields == "*":
            sql = "select * from %s" % (tablename)
        else:
            if isinstance(fields, list):
                fields = ",".join(fields)
                sql = 'select %s from %s' % (fields, tablename)
            else:
                print("fields输入参数错误")

        # 查询条件
        claim_sql = ' where '
        if claim != '':
            for key,value in claim.items():
                claim_sql = claim_sql + key + "=" + "'" + value + "'" + " and "
        claim_sql = claim_sql + "1=1"

        # 排序条件(支持 多条件排序)
        orders_sql = " order by "
        new_order = []
        if orders != '':
            for dict in orders:
                for k,v in dict.items():
                    item = k+"("+v+")"
                    new_order.append(item)
            if isinstance(new_order, list):
                orders_sql = orders_sql + ",".join(new_order)
        else:
            orders_sql = ''
        sql = sql + claim_sql + orders_sql
        print("SQL查询语句：",sql)

        # 2、获得连接
        self.getconn()

        # 3、创建游标
        cursor = self.get_cursor()

        try:
            # 4、执行SQL语句
            rows = cursor.execute(sql)
            # 5、获取所有记录列表
            if rows > 0:
                results = cursor.fetchall()
            else:
                results = ''
        except:
            print("查询语句异常")
        # 6、关闭连接
        self.close_db()

        return results

    # 查询语句(一条结果)
    def QueryOne(self):


        return None

    # insert_beat_many(sql=sql, list_tuple=list_tuple)
    # 批量插入 节奏特征(用于原声识别)
    def insert_beat_many(self, sql, list_tuple):
        # 1、获得连接
        self.getconn()
        # 2、创建游标
        cursor = self.get_cursor()
        check_sql = "select * from original_voice where song_address=%s"  # 用于检验歌曲在数据库中是否已经存在
        try:
            # 3、执行插入SQL语句
            for i in list_tuple[::]:
                # 先检验数据是否存在
                rows = cursor.execute(check_sql, i[1])
                if rows > 0:  # 已存在，则删除
                    list_tuple.remove(i)
            if list_tuple:  # 存在值即为真
                cursor.executemany(sql, list_tuple)  # 执行批量插入
                print("数据插入成功", list_tuple)
        except Exception as e:
            # 执行SQL失败，则回滚事务
            self.db.rollback()
            print('操作失败', e)
        # 5、关闭连接
        self.db.commit()
        self.close_db()
        return None
    # 批量插入 旋律特征(用于旋律识别)
    def insert_melody_many(self, sql, list_tuple):
        # 1、获得连接
        self.getconn()
        # 2、创建游标
        cursor = self.get_cursor()
        check_sql = "select * from melody where song_address=%s"  # 用于检验歌曲在数据库中是否已经存在
        try:
            # 3、执行插入SQL语句
            for i in list_tuple[::]:
                # 先检验数据是否存在
                rows = cursor.execute(check_sql,i[1])
                if rows > 0: # 已存在，则删除
                    list_tuple.remove(i)
            if list_tuple:  # 存在值即为真
                cursor.executemany(sql, list_tuple) # 执行批量插入
                print("数据插入成功", list_tuple)
        except Exception as e:
            # 执行SQL失败，则回滚事务
            self.db.rollback()
            print('操作失败', e)
        # 5、关闭连接
        self.db.commit()
        self.close_db()

        return None

    # 批量插入 song_feature
    def insert_feature_many(self, sql, list_tuple):
        # 1、获得连接
        self.getconn()
        # 2、创建游标
        cursor = self.get_cursor()
        check_sql = "select * from song_feature where song_id=%s and song_address=%s"  # 用于检验歌曲在数据库中是否已经存在
        try:
            # 3、执行插入SQL语句
            for i in list_tuple[::]:
                # 先检验数据是否存在
                rows = cursor.execute(check_sql, (i[0], i[1]))
                if rows > 0:  # 已存在，则删除
                    list_tuple.remove(i)
            if list_tuple:  # 存在值即为真
                cursor.executemany(sql, list_tuple)  # 执行批量插入
                print("插入成功", list_tuple)
        except Exception as e:
            # 执行SQL失败，则回滚事务
            self.db.rollback()
            print('操作失败', e)
        # 5、关闭连接
        self.db.commit()
        self.close_db()

        return None

    # 操作数据
    def operate_dateByCount(self, sql, count):
        """
        批量插入数据，并附带检验是否已存在
        :param sql: 插入SQL语句
        :param count: 插入条件
        :param check_sql: 检验是否存在SQL语句
        :return: 结果集
        """
        # 获得连接
        self.getconn()
        try:
            # 创建游标
            cursor = self.get_cursor()
            # 执行SQL
            check_sql = "select * from songs where song_name=%s and song_singer=%s" # 用于检验歌曲在数据库中是否已经存在
            if type(count) is tuple:  # count参数:必须是元组
                # 检验数据是否已存在
                rows = cursor.execute(check_sql, count[:2])
                if rows > 0:  # 已存在
                    print("数据已存在")
                else:         # 不存在
                    cursor.execute(sql,count)
            elif type(count) is list: # count参数:列表元素必须是元组
                '''
                for循环中删除或插入列表元素 带来的问题
                    count[::] : 当对count进行插入和删除元素时索引值会发生变化,
                    例如：
                        count = [('Tom',0),('Tom1',1),('Tom1',1),('Tom3',3)]
                        for i in count: # 当对 y 进行插入和删除元素时，y[::] 的索引和初始y的一致
                            if i == ('Tom1',1):
                                count.remove(i)
                        print("c:",count)
                        运行结果：
                            c: [('Tom', 0), ('Tom1', 1), ('Tom3', 3)]
                    解决方案：
                        count[::] 的索引和初始count的一致
                '''
                for i in count[::]:
                    # 检验数据是否已存在
                    rows = cursor.execute(check_sql, i[:2])
                    if rows > 0:  # 已存在,则删除该元素
                        count.remove(i)
                if count: # 存在值即为真
                    cursor.executemany(sql, count)
            else:
                print('参数count类型不正确')
            # 执行SQL成功，则提交事务
            self.db.commit()
            print(count, '操作成功')
            return 0
        except Exception as e:
            # 执行SQL失败，则回滚事务
            self.db.rollback()
            print('操作失败', e)
        # 关闭连接
        self.close_db()

