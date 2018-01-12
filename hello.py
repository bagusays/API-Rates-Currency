from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import tzlocal
import requests
import urllib.parse as urlparse

app = Flask(__name__)

base_url = "http://www.x-rates.com/"

def convertTime(findTime):
    local_timezone = tzlocal.get_localzone()
    utc_time = datetime.strptime(findTime[0:18], "%b %d, %Y %H:%M")
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_time

def getTable(paramTo = "IDR"):
    result = {}
    url = requests.get(base_url + "table/?from=%s&amount=1" %paramTo)
    soup = BeautifulSoup(url.text, "html.parser")
    findTime = soup.find("span", {'class': 'ratesTimestamp'}).text
    findTable = soup.find("table", {'class': 'tablesorter ratesTable'})
    result['updatedTime'] = convertTime(findTime)
    result['status'] = url.status_code
    result['table'] = findTable
    return result

@app.route("/")
def getAllCurrency():
    getSoup = getTable()
    result = {}

    r = []
    for row in getSoup['table'].findAll("tr"):
        print(row)
        cell = row.findAll("td")
        if len(cell) == 3:
            parse = urlparse.urlparse(cell[2].find("a", href=True)['href'])
            resultParam = urlparse.parse_qs(parse.query)['from'][0]
            r.append({
                'Code'  : resultParam,
                'Name'  : cell[0].text,
                'Price': float(cell[1].text),
                'PriceInverted' : float(round(float(cell[2].text),2))
            })

    result['status'] = getSoup['status']
    result['updatedTime'] = getSoup['updatedTime']
    result['result'] = r

    return jsonify(result)

@app.route("/specify")
def specifyCurrency():
    qParamFrom = request.args.get('from')
    qParamTo = request.args.get('to')
    getSoup = getTable(qParamTo)
    if qParamTo == None and qParamTo == None:
        r = []
        for row in getSoup['table'].findAll("tr"):
            cell = row.findAll("td")
            if len(cell) == 3:
                parse = urlparse.urlparse(cell[2].find("a", href=True)['href'])
                resultParam = urlparse.parse_qs(parse.query)['from'][0]
                r.append({
                    'Code'      : resultParam,
                    'Name': cell[0].text
                })
        return jsonify({'HowToUse' : 'specify?from=CODE&to=CODE', 'Code' : r})

    result = {}
    r = []
    for row in getSoup['table'].findAll("tr"):
        cell = row.findAll("td")
        if len(cell) == 3:
            parse = urlparse.urlparse(cell[2].find("a", href=True)['href'])
            resultParamFrom = urlparse.parse_qs(parse.query)['from'][0]
            resultParamTo = urlparse.parse_qs(parse.query)['to'][0]
            if resultParamFrom == qParamFrom and resultParamTo == qParamTo:
                r.append({
                    'Code': resultParamFrom,
                    'Name': cell[0].text,
                    'To': resultParamTo,
                    'PriceInverted': float(cell[1].text),
                    'Price': float(cell[2].text)
                })

    if len(r) == 0:
        result['result'] = "Currency Not Found"
    else:
        result['result'] = r

    result['status'] = getSoup['status']
    result['updatedTime'] = getSoup['updatedTime']

    return jsonify(result)

if __name__ == "__main__":
    app.run()
