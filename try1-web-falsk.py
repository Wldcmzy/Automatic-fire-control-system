from flask import Flask, request, make_response, render_template
from flask_cors import CORS
from pybase import dataSR
from pybase import dataformer
import threading

# 可变配置
active_port = 5000
targetAddr = ('8.130.23.101', 27013)

# 实例化对象/必要全局变量/必要配置
sr = dataSR.SR()
sr.receive()
df = dataformer.DataFormer()
app = Flask(__name__)
CORS(app, supports_credentials=True)
lastData = ''
rep_type_num = 5


@app.route('//msg_srer', methods = ['GET', 'POST'])
def msg_srer():
    if request.method in ['GET', 'POST']:
        res = make_response('ok')
        res.status = '200'
        #print('headers : ' , request.headers)
        lastData = str(request.headers['data'])
        send(lastData)

        #res.headers['Access-Control-Allow-Origin'] = '*'
        #res.headers['Access-Control-Allow-Headers'] = '*'
        #res.headers['Access-Control-Allow-Methods'] = '*'
        
        return res

def send(data, idx = [0, 1, 2, 3, 4]):
    df.setDic(data)
    lst = df.formReport()
    for i in idx:
        sr.send(lst[i], targetAddr)

def reSend():
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
                erridx = list(range(1, rep_type_num + 1))
            else:
                Fcode, data = data
                if data ==  dataformer.DataFormer._ReportError_dis_crce:
                    #print('数传输异常: send')
                    print('CRC error: send')
                    erridx = list(range(1, rep_type_num + 1))
                elif data == dataformer.DataFormer._ReportError_func:
                    #print('功能码异常: ' + str(hex(Fcode)))
                    print('Fcode error')
                    if Fcode not in erridx :
                        erridx.append(Fcode)
                else:
                    print('Normal: ' + str(hex(Fcode)))
            if len(erridx) != 0:
                send(lastData, erridx)
                erridx = []

t = threading.Thread(target = reSend, name = 'resend')
t.start()
app.run(host = '127.0.0.1', port = active_port, threaded = True)