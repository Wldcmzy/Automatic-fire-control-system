from flask import Flask, request, make_response
from flask_cors import CORS
from pybase import dataSR
from pybase import dataformer
import threading
import time
import json
from typing import List

# 可变配置
active_port = 5000
targetAddr = ('8.130.23.101', 27013)



# 实例化对象/必要全局变量/必要配置
lastErr = int(time.time())
sr = dataSR.SR()
sr.receive()
df = dataformer.DataFormer()
app = Flask(__name__)
CORS(app, supports_credentials=True)
lastData = {}
rep_type_num = 5



@app.route('//msg_srer', methods = ['GET', 'POST'])
def msg_srer() -> None:
    global lastErr
    if request.method in ['GET', 'POST']:
        res = make_response('ok')
        res.status = '200'
        #print('headers : ' , request.headers)
        tmp = json.loads(str(request.headers['data']))
        area = tmp['fq']['area']
        lastData[area] = tmp
        send(lastData[area])
        nowErr = int(time.time())
        if nowErr - lastErr > 27:
            time.sleep(1)
            send(lastData[area], [0, 1, 2, 3, 4], True) # 参数error 为True, 表示定时手动制造错误
            lastErr = nowErr

        #res.headers['Access-Control-Allow-Origin'] = '*'
        #res.headers['Access-Control-Allow-Headers'] = '*'
        #res.headers['Access-Control-Allow-Methods'] = '*'
        
        return res

def send(data, idx : List[int] = [0, 1, 2, 3, 4], err : bool = False) -> None:
    '''数据发送'''
    df.setDic(data)
    lst = df.formReport()
    if err == True: # 手动制造一个CRC错误
        print('send Err msg...')
        ecrc = chr((ord(lst[2][-2]) + 100) % 256)
        lst[2] = lst[2][ : -2] + ecrc + lst[2][-1]
    for i in idx:
        if i < len(lst):
            sr.send(lst[i], targetAddr)


def reSend() -> None:
    '''错误数据重传, 这个函数应在额外线程中执行'''
    erridx = []
    while True:
        data = sr.getData()
        if data != None:
            #print('接收到数据', end = ' >>> ')
            print('message recived', end = ' >>> ')
            data = df.parseReplay(data[0])
            if data == dataformer.DataFormer._ReportError_crce: # 数据未能解析
                #print('数传输异常: receive')
                print('CRC error: receive')
                erridx = list(range(rep_type_num))
            else:
                Fcode, data = data
                if data ==  dataformer.DataFormer._ReportError_dis_crce:
                    #print('数传输异常: send')
                    print('CRC error: send')
                    erridx = list(range(1, rep_type_num + 1))
                elif data == dataformer.DataFormer._ReportError_func:
                    #print('功能码异常: ' + str(hex(Fcode)))
                    print('Fcode error')
                    assert Fcode in dataformer.DataFormer._Fcodes
                    Eid = dataformer.DataFormer._Fcodes.index(Fcode)
                    if Eid not in erridx :
                        erridx.append(Eid)
                else:
                    print('Normal: ' + str(hex(Fcode)))
            if len(erridx) != 0:
                print('try reSend...')
                for key, value in lastData.items():
                    send(value, erridx, False)
                erridx = []

# 开启resend线程
t = threading.Thread(target = reSend, name = 'resend')
t.start()
app.run(host = '127.0.0.1', port = active_port, threaded = True)