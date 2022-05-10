import pymysql
class sqlOperator:
    def __init__(self, host, user, password, database):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
    
    def active(self):
        self.__connection = pymysql.connect(host = self.__host, user = self.__user, password = self.__password, database = self.__database)
        self.__cursor = self.__connection.cursor(cursor=pymysql.cursors.DictCursor)

    def inactive(self):
        self.__connection.close()
        self.__cursor.close()

    def add_fe05(self, area, id, status):
        nameT = 'fe05'
        sql = 'insert into %s values (%s, %s, %s)'
        self.__cursor.execute(sql, (nameT, area, id, status))
        self.__connection.commit()