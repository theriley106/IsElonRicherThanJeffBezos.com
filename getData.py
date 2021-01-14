import requests
import os
try:
    from keys import *
except:
    API_KEY = os.environ['API_KEY']
import time
import json

RANKING_URL = "https://www.forbes.com/forbesapi/person/rtb/0/-estWorthPrev/true.json?fields=rank,personName,finalWorth,estWorthPrev,uri"
QUOTE_URL = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={0}&apikey={1}"

JEFF_BEZOS_SHARES = 54318411
ELON_MUSK_SHARES = 34098597

ELON_NW_NO_STOCK = (183763.418 * 1000000) - (ELON_MUSK_SHARES * 849.44)
BEZOS_NW_NO_STOCK = (182416.835 * 1000000) - (JEFF_BEZOS_SHARES * 3120.83)

def get_share_price(ticker):
    for i in range(3):
        try:
            return float(requests.get(QUOTE_URL.format(ticker, API_KEY)).json()['Global Quote']["05. price"])
        except Exception as exp:
            time.sleep(i + 1)

def get_ranking():
    for i in range(3):
        try:
            return requests.get(RANKING_URL).json()["personList"]["personsLists"]
        except Exception as exp:
            time.sleep(i + 1)
    return []


if __name__ == "__main__":
    bezos_nw = (BEZOS_NW_NO_STOCK + (get_share_price('AMZN') * JEFF_BEZOS_SHARES)) / 1000000
    elon_nw = (ELON_NW_NO_STOCK + (get_share_price('TSLA') * ELON_MUSK_SHARES)) / 1000000
    ranking = []
    for val in get_ranking():
        if val['uri'] == 'jeff-bezos':
            val['finalWorth'] = bezos_nw
        if val['uri'] == 'elon-musk':
            val['finalWorth'] = elon_nw
        ranking.append(val)
    ranking.sort(key=lambda k: k['finalWorth'], reverse=True)
    for i, val in enumerate(ranking):
        val['rank'] = i + 1
    
    if len(ranking) != 0:
        response = {
            "ranking": ranking[:5],
            "updated_at": time.time()
        }
        with open('response.json', 'w') as f:
            json.dump(response, f, indent=4)