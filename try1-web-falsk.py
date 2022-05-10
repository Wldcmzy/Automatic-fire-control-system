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
erridx = []


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
    while True:
        data = sr.getData()
        if data != None:
            data = data[0]
            for each in data:
                print(hex(ord(each)), end = '')
            print()

t = threading.Thread(target = reSend, name = 'resend')
t.start()
app.run(host = '127.0.0.1', port = active_port, threaded = True)