# step1: import pymysql module
import pymysql

# step2: connect to the database
con = pymysql.connect(host="localhost", 
                      port=3306, 
                      username='root', 
                      password='123456Pa!',
                      database='',#unnecessary
                      charset='utf-8' #unnecessary)

# step3: create a cursor
cur = conn.cursor()

# step4: execute sql code: saerch
sql = "SELECT * FROM students"
res = sur.execute(sql)

# show volume of data
print(res)

# show one data,return tuple
data1 =cur.fetchone()
print(data1)

# show all datas,return tuple
datas = cur.fetchall()
print()


# step 4:execute sql code:insert
# when executing delete/insert/modify transaction, pymysql would open automatically
# but if you don't submit transaction, it dosen't effective.
sql = "insert into students value(0,'musen',18,180,2,1,0)"
res = cur.execute(sql)
# submit transaction
cur.commit()

# step 5:close connection and cursor
cur.close()
conn.close()



