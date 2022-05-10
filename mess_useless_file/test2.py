from flask import Flask, request, make_response, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/test2', methods = ['GET', 'POST'])
def form():
    if request.method in ['GET', 'POST']:
        res = make_response('abcdefG-||')
        res.status = '202'
        res.headers['Access-Control-Allow-Origin'] = '*' 
        res.headers['Access-Control-Allow-Headers'] = '*'
        res.headers['test'] = 'Test txt'
        return res
    elif request.method == 'POST':
        pass

if __name__ == '__main__':
    app.run()