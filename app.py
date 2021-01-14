from flask import Flask, render_template, jsonify
import json
import getData

app = Flask(__name__, static_url_path='/static')

@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.0f}".format(value * 1000000)
    
@app.route('/', methods=['GET'])
def index():
    ranking = getData.get_from_mongo().get('ranking', [])
    if len(ranking) < 5:
        return 'error', 404
    return render_template("index.html", ranking=ranking, result=ranking[0]["personName"] == "Elon Musk")

@app.route('/no', methods=['GET'])
def indexno():
    ranking = getData.get_from_mongo().get('ranking', [])
    if len(ranking) < 5:
        return 'error', 404
    return render_template("index.html", ranking=ranking, result=ranking[0]["personName"] != "Elon Musk")

@app.route('/debug', methods=['GET'])
def debug():
    return jsonify(getData.get_from_mongo())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)