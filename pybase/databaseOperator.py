from time import time
import pymysql
class sqlOperator:
    def __init__(self, host, user, password, database):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
    
    # 激活对象
    def active(self):
        self.__connection = pymysql.connect(host = self.__host, user = self.__user, password = self.__password, database = self.__database)
        self.__cursor = self.__connection.cursor(cursor=pymysql.cursors.DictCursor)

    # 关闭对象功能
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
    
    # 获取某区域一段时间内的消息
    def select_span(self, area, low, high):
        area = int(area)
        timelst = self.getTimeSPANby_sys01(area, low, high)
        #print(timelst)
        ret = []
        for each in timelst:
            ret.append(self.select_byTime(area, int(each['sendTime'])))
        return ret

    # 获取某区域最新消息
    def select_newest(self, area):
        area = int(area)
        tm = self.select_newest_by_sys01(area)['sendTime']
        #print('new : ', tm)
        assert tm != None
        return self.select_byTime(area, int(tm))

    # 获取区域在某时间的消息  
    def select_byTime(self, area, tm):
        dic = {
            1 : self.select_table('sys01', area, tm),
            2 : self.select_table('gz02', area, tm),
            3 : self.select_table('fq03', area, tm),
            4 : self.select_table('f04', area, tm),
            5 : self.select_table('fe05', area, tm),
        }
        return dic

    # 获取某区域所有数据的发送时间 
    def getTimeLSTby_sys01(self, area):
        nameT, arg = 'sys01', 'sendTime'
        sql = 'select sendTime from %s where AREA = %d order by %s desc' % (nameT, area, arg)
        cnt = self.__cursor.execute(sql)
        if cnt <= 0 : return None
        return self.__cursor.fetchall()

    # 获取某区域一段时间内的数据发送时间
    def getTimeSPANby_sys01(self, area, low, high):
        nameT = 'sys01'
        #print(type(area),type(low), type(high))
        sql = 'select sendTime from %s where AREA = %d and sendTime >= %d and sendTime <= %d' % (nameT, area, low, high)
        cnt = self.__cursor.execute(sql)
        if cnt <= 0 : return None
        return self.__cursor.fetchall()

    # 获取某区域最新发送数据的时间
    def select_newest_by_sys01(self, area):
        return self.getTimeLSTby_sys01(area)[0]

    # 查询存在某表中的某区域某时间发送的消息
    def select_table(self, nameT, area, tm):
        sql = 'select * from %s where AREA = %d and sendTime = %d' % (nameT, area, tm)
        cnt = self.__cursor.execute(sql)
        if cnt <= 0 : return []
        ret = self.__cursor.fetchall()
        self.__connection.commit()
        return ret

# 数据解析
# def parseData(dic):
#     d1 = dic[1][0]
#     d3 = dic[3][0]
#     d4 = dic[4][0]
#     ret = ''
#     ret += '时间戳:%s ' % d1['sendTime']
#     ret += '防护区:%d 控制状态:%s\n' % (d1['AREA'], '自动' if d3['auto'] == True else '手动')
#     ret += '警报数量:%d 故障数量:%d 探测器数量:%d 灭火器数量: %d' %(d1['JBnum'], d1['GZnum'], d1['Fnum'], len(dic[5]))
#     ret += '喷洒状态:%s\n' % ('正在喷洒' if d3['rain'] == True else '未喷洒')
#     ret += '分区环境信息:\n'
#     ret += '温度: %.3f摄氏度 CO: 百分之%.3f VOC: %.3fg/L 烟雾:%.3fmg/立方米\n' % (d4['oc'], d4['co'], d4['voc'], d4['fog'])
#     ret += '故障机器号:'
#     if len(dic[2]) == 0:
#         ret += '(无故障机器)'
#     for each in dic[2]:
#         ret += each['id'] + ' '
#     ret += '\n'
#     return ret