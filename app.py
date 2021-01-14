from flask import Flask, render_template, jsonify
import os
import json

app = Flask(__name__, static_url_path='/static')

RESPONSE = {}
FILE_NAME = 'response.json'

@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.0f}".format(value * 1000000)

def get_updated_time(fileName):
    try:
        return int(os.path.getmtime(fileName))
    except:
        return None

def get_net_worth():
    last_updated = RESPONSE.get('updated_at', 0)
    if get_updated_time(FILE_NAME) != RESPONSE.get('modified', 0):
        if os.path.exists(FILE_NAME):
            RESPONSE['response'] = json.load(open(FILE_NAME))
            RESPONSE['modified'] = get_updated_time(FILE_NAME)
    return RESPONSE.get('response', {})
    
@app.route('/', methods=['GET'])
def index():
    ranking = get_net_worth().get('ranking', [])
    if len(ranking) < 5:
        return 'error', 404
    return render_template("index.html", ranking=ranking, result=ranking[0]["personName"] == "Elon Musk")

@app.route('/no', methods=['GET'])
def indexno():
    ranking = get_net_worth().get('ranking', [])
    if len(ranking) < 5:
        return 'error', 404
    return render_template("index.html", ranking=ranking, result=ranking[0]["personName"] != "Elon Musk")

@app.route('/debug', methods=['GET'])
def debug():
    return jsonify(get_net_worth())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)