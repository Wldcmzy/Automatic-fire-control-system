from flask import Flask, request, make_response, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('//sch', methods = ['GET', 'POST'])
def sch():
    #res = make_response('ok')
    #res.status = '200'
    return 'hello' 

app.run(host = '0.0.0.0', port = 27777, threaded = True)
