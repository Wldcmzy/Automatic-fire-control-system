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

    def add_fe05(self, tm, revID, dic):
        nameT = 'fe05'
        sql = 'insert into %s values (\'%s\', %d, %d, %d, %d)' % (nameT, revID, dic['area'], dic['id'], dic['work'], tm)
        self.__cursor.execute(sql)
        self.__connection.commit()

    def add_f04(self, tm, revID, dic):
        nameT = 'f04'
        sql = 'insert into %s values (\'%s\', %d, \'%s\', %d, %d, %f, %f, %f, %f, %d)' % (nameT, revID, dic['area'], dic['Mtype'], dic['Mid'], dic['JBlevel'], dic['oc'], dic['co'], dic['voc'], dic['fog'], tm)
        self.__cursor.execute(sql)
        self.__connection.commit()

    def add_fq03(self, tm, revID, dic):
        nameT = 'fq03'
        sql = 'insert into %s values (\'%s\', %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)' % (nameT, revID, dic['area'], dic['JBlevel'], dic['GZ'], dic['auto'], dic['NOTauto'], dic['start'], dic['shutdown'], dic['rain'], dic['startRain'], tm)
        self.__cursor.execute(sql)
        self.__connection.commit()
        
    def add_gz02(self, tm, revID, dic):
        nameT = 'gz02'
        sql = 'insert into %s values (\'%s\', %d, \'%s\', %d, %d, %d)' % (nameT, revID, dic['area'], dic['type'], dic['id'], dic['GZcode'], tm)
        self.__cursor.execute(sql)
        self.__connection.commit()

    def add_sys01(self, tm, revID, dic):
        nameT = 'sys01'
        sql = 'insert into %s values (\'%s\', %d, %d, %d, %d, %d)' % (nameT, revID, dic['area'], dic['JBnum'], dic['GZnum'], dic['FeelerNum'], tm)
        self.__cursor.execute(sql)
        self.__connection.commit()
        