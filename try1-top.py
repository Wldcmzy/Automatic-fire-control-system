from pybase import dataSR
from pybase import dataformer
from pybase import databaseOperator
import time
import cfg


host = cfg.Ghost
user = cfg.Guser
psd = cfg.Gpsd
db = cfg.Gdb

# 实例化必要对象
op = databaseOperator.sqlOperator(host, user, psd, db)
op.active()
df = dataformer.DataFormer()
sr = dataSR.SR()
sr.receive()

IterNum, IterMax = 0, 0x7fffffff

def v2t(num, leng = 2) -> str:
    '''补0函数, 使用与from_revID'''
    ret = str(num)
    if len(ret) > leng: return None
    return '0' * (leng - len(ret)) + ret

def form_revID(const_time = None) -> str:
    '''按照接收到的时间和迭代数组合,为要存入数据库的消息生成主键值'''
    global IterMax, IterNum
    IterNum = (IterNum + 1) % IterMax
    if const_time != None: 
        tm = const_time
    else:
        tm = time.localtime()[ : 6]
    ret = v2t(tm[0], 4)
    for each in tm[1 : 6]: ret += v2t(each)
    ret += str(IterNum)
    return ret


#  数据接收和数据库处理功能 主干
while True:
    address = ''
    data = sr.getData()
    if data != None:
        data, address = data
        data = df.parseReport(data)
        #print(data)
        data, dic = data
        print('接收到消息 Fcode:%#X ID:%d Time:%d' % (dic['Fcode'], dic['id'], dic['time']))
        if data == dataformer.DataFormer._ReportError_unkn:
            data = df.formReplay(dic['Fcode'], dic['id'], True, dataformer.DataFormer._dicErr2Num['unkn'])
            print('消息接受出错:', dataformer.DataFormer._ReportError_unkn)
        elif data == dataformer.DataFormer._ReportError_read:
            data = None
            print('消息接受出错:', dataformer.DataFormer._ReportError_read)
        elif data == dataformer.DataFormer._ReportError_crce:
            data = df.formReplay(dic['Fcode'], dic['id'], True, dataformer.DataFormer._dicErr2Num['crce'])
            print('消息接受出错:', dataformer.DataFormer._ReportError_crce)
        elif data == dataformer.DataFormer._ReportError_func:
            data = df.formReplay(dic['Fcode'], dic['id'], True, dataformer.DataFormer._dicErr2Num['func'])
            print('消息接受出错:', dataformer.DataFormer._ReportError_func)
        else:
            tm = dic['time']
            if dic['Fcode'] == 0xa0:
                t = time.localtime()[ : 6]
                for each in data:
                    op.add_fe05(tm, form_revID(t), each)
            elif dic['Fcode'] == 0x90:
                op.add_f04(tm, form_revID(t), data)
            elif dic['Fcode'] == 0x80:
                op.add_fq03(tm, form_revID(t), data)
            elif dic['Fcode'] == 0x70:
                t = time.localtime()[ : 6]
                for each in data['values']:
                    op.add_gz02(tm, form_revID(t), each)
            elif dic['Fcode'] == 0x60:
                op.add_sys01(tm, form_revID(t), data)

            
            print('消息正确接受,并存入数据库...')
            data = df.formReplay(dic['Fcode'], dic['id'], False, 0)

        if data != None:
            sr.send(data, address)
else:
    op.inactive()