import pymysql as ps

# revised by mjs at 2019.12.16
class SQLI(object):
    def __init__(self, user, psd, db1):
        '''
        init process:create connection and cursor
        '''
        self.conn = ps.connect(host='localhost',
                        port=3306,
                        user=user,
                        password=psd,
                        db=db1)
        self.cur = self.conn.cursor()
        try:
            sql = "set interactive_timeout=24*3600"
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
    
    def startTrans(self):
        sql = 'SET autocommit=0;'
        sql1 = 'START TRANSACTION'
        self.cur.execute(sql)
        self.cur.execure(sql1)
 
    def find(self, sql):
        '''
        search process
        return result tuple
        '''
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            #return False

    def add_column(self, table, columns, types):
        '''
        :param table:table name
        :param columns: column name list
        :param types: column type list
        :return:
        '''
        try:
            sql = 'alter table ' + table
            for column, type in zip(columns, types):
                sql += ' add {} {},'.format(column, type)
            sql = sql[0:sql.rfind(',')] + ';'
            res = self.cur.execute(sql)
            self.conn.commit()
            return res
        except Exception as e:
            print('Add feild: {}'.format(e))
            self.conn.rollback()

    def update_data(self, sql):
        '''
        update process
        '''
        try:
            # startTrans()
            res = self.cur.execute(sql)
            if res==0:
                print("update fail")
            else:
                # 提交事务
                self.conn.commit()
                print("update success!")
            return res   # 可以不返回
        except Exception as e:
            print(e)
            self.conn.rollback()
              
    def close(self):
        '''
        关闭数据库连接和游标
        '''    
        self.cur.close()
        self.conn.close()
