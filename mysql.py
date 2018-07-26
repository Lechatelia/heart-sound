#coding:utf-8
import pymysql
import datetime
table_name='USE_INF'
cols={'username':'USE_NAME','user_age':'USE_AGE','user_sex':'USE_SEX','user_birthdar':'USE_BIR'}

Server=["132.232.3.244", "root", "hx37241", "renesa"]

#注意
# "VALUES ('%s',  %d ,%d ,%d)" \
#     '%s'引号是必须的，不然认不出来是字符

class Mysql():
    def __init__(self):
        self.table=table_name
        self.col=cols

    def connect(self,ip,users,password,sqlname):
        self.db= pymysql.connect(ip,users,password,sqlname)

    def show_version(self):
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = self.db.cursor()
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT VERSION()")
        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchone()
        print("Database version : %s " % data)

    def show_Info(self):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # SQL 查询语句
        sql = "SELECT * FROM USE_INFMATION "
        try:
            # 执行SQL语句s
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            print("--------------------------------------------------")
            for row in results:
                print("|%d\t\t%s\t\t|%s\t\t|%d\t\t|%d\t\t|" % \
                      (row[0], row[1], row[2], row[3],row[4]))
                      # (row[0], row[1], row[2].strftime("%Y-%m-%d"), row[3],row[4]))
            print("--------------------------------------------------")
        except:
            print("Error: unable to fetch data")

    def show_conclusion(self):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # SQL 查询语句
        sql = "SELECT * FROM CONCLUSION "
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            print("--------------------------------------------------")
            for row in results:
                print("|%d\t\t|%s\t\t|%5f\t\t|%s\t\t\t|%s\t\t|" % \
                      (row[0], row[1], row[2], row[3],row[4]))
            print("--------------------------------------------------")
        except:
            print("Error: unable to fetch data")


    def Insert_info_old(self,info):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # SQL 插入语句
        sql = "INSERT INTO " \
              "USE_INF(USE_NAME,USE_AGE, USE_SEX,USE_BIR) " \
              "VALUES ('%s',  %d ,%d ,%d)" \
              %((info[0]),info[1],info[2],info[3])
            # .format(name=info[0], age=info[1],sex=info[2],birthday=info[3])
        # sql='INSERT INTO USE_INF(USE_NAME,USE_AGE, USE_SEX,USE_BIR) VALUES ("boy",  20 ,1 ,19970345)'
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

    def Insert_User_Info(self,info):
        # [1234567890,'boy1', '1997-03-27' ,1 ,13772052853]
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # SQL 插入语句

        sql="INSERT INTO USE_INFMATION (USE_ID,USE_NAME,USE_BRI, USE_SEX,USE_TEL) VALUES (%d,'%s', '%s' ,%d,%d)"%(info[0],info[1],info[2],info[3],info[4])
        # sql="INSERT INTO USE_INFMATION (USE_ID,USE_NAME,USE_BRI,USE_SEX,USE_TEL)  VALUES (1567890,'abc',1,13772052853)"
        # sql="""INSERT INTO USE_INFMATION VALUES ('123456789','abc', '1997-03-27','1' ,'13772051234')"""
        try:
            # 执行sql语句Error: unable to fetch data
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

    def Insert_Diagnosis(self,info):
        #[1234567890,"normal",0.998,'normal.wav']
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # SQL 插入语句

        sql="INSERT INTO CONCLUSION (USE_ID,RESULT,POSSIBLITY, DATETIME,WAV_INF) VALUES (%d,'%s','%f',NOW(),'%s')"%(info[0],info[1],info[2],info[3])
        try:
            # 执行sql语句Error: unable to fetch data
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

    def Delete_by_name_old(self,name):
        # SQL 删除语句
        cursor = self.db.cursor()
        sql = "DELETE FROM USE_INF WHERE USE_NAME = '%s'" % (name)
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 提交修改
           self.db.commit()
        except:
           # 发生错误时回滚
           self.db.rollback()
    #
    def Delete_Info_by_ID(self,ID):
        # SQL 删除语句
        cursor = self.db.cursor()
        sql = "DELETE FROM USE_INFMATION WHERE USE_ID = '%s'" % (ID)
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 提交修改
           self.db.commit()
        except:
           # 发生错误时回滚
           self.db.rollback()

    def Delete_Diagnosis_by_ID(self,ID):
        # SQL 删除语句
        cursor = self.db.cursor()
        sql = "DELETE FROM CONCLUSION WHERE USE_ID = '%s'" % (ID)
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 提交修改
           self.db.commit()
        except:
           # 发生错误时回滚
           self.db.rollback()

    def Update_birth_by_name(self,name,changr):
        cursor = self.db.cursor()
        sql=" UPDATE USE_INF SET USE_BIR='%d'   WHERE USE_NAME='%s' "%(changr,name)
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 提交修改
           self.db.commit()
        except:
           # 发生错误时回滚
           self.db.rollback()

    def Add_ALTER(self):
        # 该函数需要自己更改
        cursor = self.db.cursor()
        sql="ALTER TABLE USE_INF  ADD  USE_Time DATETIME()"
        # sql="ALTER TABLE USE_INF  ALTER COLUMN  USE_BIR INT(8)"
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 提交修改
           self.db.commit()
        except:
           # 发生错误时回滚
           self.db.rollback()

    def close_sql(self):
        # 关闭数据库连接
        self.db.close()

def Add_info_to_SQL(ID=1234567890,Name='XJTUer',Birthday='1997-03-27',sex=1,tel=13712345678):
    mysql=Mysql()
    mysql.connect(Server[0], Server[1], Server[2], Server[3])
    mysql.Insert_User_Info([ID,Name, Birthday ,sex ,tel])
    mysql.close_sql()

def Add_Diagnosis_to_SQL(ID=1234567890,Result='normal',Possi=0.512345,wav_dir='./normal.wav'):
    mysql=Mysql()
    mysql.connect(Server[0], Server[1], Server[2], Server[3])
    mysql.Insert_Diagnosis([ID,Result,Possi,wav_dir])
    mysql.close_sql()

def SQL_test():
    time =str(datetime.datetime.now()).split('.')[0]
    mysql=Mysql()
    mysql.connect("132.232.3.244", "root", "hx37241", "renesa")


    mysql.Delete_Info_by_ID('1234567890')
    mysql.Insert_User_Info([1234567890,'boy1', '1997-03-27' ,1 ,13772052853])

    mysql.Delete_Diagnosis_by_ID(123124312)
    mysql.Insert_Diagnosis([123124312,"normal",0.57801119,'./normal.wav'])

    mysql.show_Info()
    mysql.show_conclusion()
    mysql.close_sql()



if __name__=='__main__':
    Add_info_to_SQL(1234888821,'Peter','1972-01-02',0,13785266548)
    Add_Diagnosis_to_SQL(1234888821,'murmur',0.765854,'./murmur.wav')
    SQL_test()



