from flask import Flask, request, make_response, render_template, url_for, jsonify
from flask_cors import CORS
from pybase import databaseOperator
import json
import threading
import cfg

host = cfg.Ghost
user = cfg.Guser
psd = cfg.Gpsd
db = cfg.Gdb


app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/newest', methods = ['POST'])
def newest():
    '''相应获取某区域最新数据的请求'''
    data = json.loads(request.headers['data'])
    #print(data, type(data))
    area, id = int(data['area']), int(data['id'])
    print('query new --', area)
    
    op = databaseOperator.sqlOperator(host, user, psd, db)
    op.active()
    try :
        ret = op.select_newest(area)
    except:
        ret = dict({'error': 'error, no area:%d maybe.' % area} )
    op.inactive()
    ret['id'] = id
    resp = make_response()
    resp.status = 200
   
    resp.headers['txt'] = 'jsjzhsjSEP' +  json.dumps(ret) + 'jsjzhsjSEP'
    # print(json.dumps(ret))
    #return jsonify(resp)
    #return json.dumps(resp)
    return resp

@app.route('/history', methods = ['POST'])
def history():
    '''相应查看某区域历史记录的请求'''
    tmerr = False
    op = databaseOperator.sqlOperator(host, user, psd, db)
    op.active()
    try:
        data = json.loads(request.headers['data'])
        area = data['area']
        timelow, timehigh = int(data['datelow']), int(data['datehigh'])
        timelow, timehigh = timelow * 100 + int(data['hourlow']), timehigh * 100 + int(data['hourhigh'])
        timelow, timehigh = timelow * 100 + int(data['minlow']), timehigh * 100 + int(data['minhigh'])
        timelow *= 100
        timehigh *= 100
    except:
        tmerr = True
    try :
        if tmerr == False:
            ret = op.select_span(area, timelow, timehigh)
        else: 
            ret = [dict({'error': 'Time input is wrong, maybe.'} )]
    except:
        ret = [dict({'error': 'error, no area:%d maybe.' % int(area)} )]
    #print(ret)
    op.inactive()
    resp = make_response()
    resp.status = 200
   
    resp.headers['txt'] = 'jsjzhsjSEP' +  json.dumps(ret) + 'jsjzhsjSEP'
    return resp

@app.route('/window', methods = ['GET'])
def window():
    return render_template('try1-top.html')

app.run(host = '0.0.0.0', port = 27777, threaded = True)
