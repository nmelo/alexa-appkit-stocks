from flask import Flask, make_response, render_template, request
import logging, json
import requests
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def post():
    logging.info(json.dumps(request.json, indent=4, sort_keys=False))

    stock_name = request.json["request"]["intent"]["slots"]["Stock"]["value"]

    logging.info("Stock name: %s" % stock_name)

    # Query API to convert name to Symbol
    name_dict = requests.get('http://dev.markitondemand.com/Api/v2/Lookup/json?input={}'.format(stock_name)).json()
    symbol = name_dict[0]["Symbol"]
    company_name = name_dict[0]["Name"]

    logging.info("Symbol: %s" % symbol)
    logging.info("Name: %s" % company_name)

    # Query API to get quote for symbol
    quote_dict = requests.get('http://dev.markitondemand.com/Api/v2/Quote/json?symbol={}'.format(symbol)).json()
    last_price = quote_dict["LastPrice"]

    logging.info("Last Price: %s" % last_price)

    # If it's after 4:00pm say closed, otherwise say current price
    # Subscribe to a notification when the price of the stock reaches something

    response = '{"version":"1.0","sessionAttributes":{"user":{"name":"nelson"}},"response":{"outputSpeech":{"type":"PlainText","text":"Today, %s closed at %s dollars."},"card":{"type":"Simple","title":"%s","subtitle":"%s closed at %s dollars.","content":""},"shouldEndSession":true}}' % (company_name, last_price, symbol, company_name, last_price)

    logging.info(json.dumps(json.loads(response), indent=4, sort_keys=False))
    return response, 200, {'Content-Type': 'application/json;charset=UTF-8'}


if __name__ == '__main__':
    app.run()

