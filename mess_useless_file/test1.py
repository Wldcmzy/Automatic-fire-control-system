from flask import Flask, request, make_response, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
@app.route('/test', methods = ['GET', 'POST'])

def form():
    print(98765)
    print(request.method)
    if request.method in ['GET', 'POST']:
        print(12345)
        res = make_response('abcdefG')
        res.status = '202'
        #res.headers['Access-Control-Allow-Origin'] = '*'
        #res.headers['Access-Control-Allow-Headers'] = '*'
        #res.headers['Access-Control-Allow-Methods'] = '*'
        return res
    elif request.method == 'POST':
        pass

if __name__ == '__main__':
    app.run()