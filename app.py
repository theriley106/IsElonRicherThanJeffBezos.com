from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import requests
import time

app = Flask(__name__, static_url_path='/static')

URL = "https://www.forbes.com/forbesapi/person/rtb/0/-estWorthPrev/true.json?fields=rank,personName,finalWorth,estWorthPrev,uri"

RESPONSE = {}
REFRESH_TIME = 5 * 60

@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.0f}".format(value * 1000000)

def get_net_worth():
    last_updated = RESPONSE.get('updated_at', 0)
    if time.time() - last_updated > REFRESH_TIME:
        try:
            res = requests.get(URL)
            ranking = sorted(res.json()["personList"]["personsLists"], key=lambda k: k['rank'])[:5]
            RESPONSE['ranking'] = ranking
            RESPONSE['updated_at'] = time.time()
        except:
            pass
    return RESPONSE
    
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)