from flask import Flask, request, make_response, render_template
from flask_cors import CORS

active_port = 5000

app = Flask(__name__)
CORS(app, supports_credentials=True)
@app.route('//msg_srer', methods = ['GET', 'POST'])
def msg_srer():
    if request.method in ['GET', 'POST']:
        res = make_response('ok')
        res.status = '200'
        #print('headers : ' , request.headers)
        with open('asdf.txt', 'w') as f:
            f.write(str(request.headers))
        
        #res.headers['Access-Control-Allow-Origin'] = '*'
        #res.headers['Access-Control-Allow-Headers'] = '*'
        #res.headers['Access-Control-Allow-Methods'] = '*'
        
        return res

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = active_port)