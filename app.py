from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import requests
import time

app = Flask(__name__, static_url_path='/static')
try:
    from keys import *
except:
    API_KEY = os.environ['API_KEY']

URL = "https://www.forbes.com/forbesapi/person/rtb/0/-estWorthPrev/true.json?fields=rank,personName,finalWorth,estWorthPrev,uri"

RESPONSE = {}
REFRESH_TIME = 5 * 60

JEFF_BEZOS_SHARES = 54318411
ELON_MUSK_SHARES = 34098597

ELON_NW_NO_STOCK = (183763.418 * 1000000) - (ELON_MUSK_SHARES * 849.44)
BEZOS_NW_NO_STOCK = (182416.835 * 1000000) - (JEFF_BEZOS_SHARES * 3120.83)

def calc_bezos():
    res = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AMZN&apikey={}".format(API_KEY))
    stock_price = float(res.json()['Global Quote']["05. price"])
    return (BEZOS_NW_NO_STOCK + (stock_price * JEFF_BEZOS_SHARES)) / 1000000

def calc_elon():
    res = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=TSLA&apikey={}".format(API_KEY))
    stock_price = float(res.json()['Global Quote']["05. price"])
    return (ELON_NW_NO_STOCK + (stock_price * ELON_MUSK_SHARES)) / 1000000

@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.0f}".format(value * 1000000)

def get_net_worth():
    last_updated = RESPONSE.get('updated_at', 0)
    if time.time() - last_updated > REFRESH_TIME:
        try:
            res = requests.get(URL)
            ranking = res.json()["personList"]["personsLists"]
            for val in ranking:
                if val['uri'] == 'jeff-bezos':
                    val['finalWorth'] = calc_bezos()
                if val['uri'] == 'elon-musk':
                    val['finalWorth'] = calc_elon()
            ranking.sort(key=lambda k: k['finalWorth'], reverse=True)
            for i, val in enumerate(ranking):
                val['rank'] = i + 1
            RESPONSE['ranking'] = ranking[:5]
            RESPONSE['updated_at'] = time.time()
        except Exception as exp:
            print(exp)
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