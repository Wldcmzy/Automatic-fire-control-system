from flask import Flask, request, make_response, render_template, url_for, jsonify
from flask_cors import CORS
from pybase import databaseOperator
import json
import threading


host = '127.0.0.1'
user = 'ks1'
psd = '1sk'
db = 'KS1'


app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/newest', methods = ['POST'])
def newest():
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

@app.route('/window', methods = ['GET'])
def window():
    return render_template('try1-top.html')

app.run(host = '0.0.0.0', port = 27777, threaded = True)
