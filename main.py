from flask import Flask, make_response, render_template, request
import logging
import json
import datetime
import requests

app = Flask(__name__)

CONTENT_TYPE = {'Content-Type': 'application/json;charset=UTF-8'}


def generate_speech(company_name, last_price):

    now = datetime.datetime.now()
    before_nine_am = now < now.replace(hour=9, minute=0, second=0)
    after_four_pm = now > now.replace(hour=16, minute=0, second=0)

    if before_nine_am:
        return "Yesterday, %s closed at %s dollars." % (company_name, last_price)
    elif after_four_pm:
        return "Today, %s closed at %s dollars." % (company_name, last_price)
    else:
        return "%s is now at %s dollars." % (company_name, last_price)


def generate_response(output_speech, card_title="", card_subtitle="", card_content="", session_attributes={}, should_end_session=True):
    response = {
        "version": "1.0",
        "sessionAttributes": {
            "user": {
                "name": "nelson"
            }
        },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": output_speech
            },
            "card": {
                "type": "Simple",
                "title": card_title,
                "subtitle": card_subtitle,
                "content": card_content
            },
            "shouldEndSession": should_end_session
        }
    }
    return json.dumps(response)


@app.route('/', methods=['GET', 'POST'])
def post():
    logging.info(json.dumps(request.json, indent=4, sort_keys=False))

    response = ""

    try:
        stock_name = request.json["request"]["intent"]["slots"]["Stock"]["value"]
    except TypeError:
        response = generate_response("Price not found.")
        return response, 200, CONTENT_TYPE

    logging.info("Stock name: %s" % stock_name)

    # Query API to convert name to Symbol
    name_dict = requests.get('http://dev.markitondemand.com/Api/v2/Lookup/json?input={}'.format(stock_name)).json()

    try:
        symbol = name_dict[0]["Symbol"]
        company_name = name_dict[0]["Name"]
    except IndexError:
        response = generate_response("Symbol not found for %s." % stock_name)
        return response, 200, CONTENT_TYPE

    logging.info("Symbol: %s" % symbol)
    logging.info("Name: %s" % company_name)

    # Query API to get quote for symbol
    quote_dict = requests.get('http://dev.markitondemand.com/Api/v2/Quote/json?symbol={}'.format(symbol)).json()
    try:
        last_price = quote_dict["LastPrice"]
    except IndexError:
        response = generate_response("Price not found for %s." % stock_name)
        return response, 200, CONTENT_TYPE

    logging.info("Last Price: %s" % last_price)

    # If it's after 4:00pm say closed, otherwise say current price
    # Subscribe to a notification when the price of the stock reaches something

    speech = generate_speech(company_name, last_price)

    response = generate_response(
        output_speech=speech,
        card_title=symbol,
        card_subtitle=speech,
        card_content="")

    logging.info(json.dumps(json.loads(response), indent=4, sort_keys=False))
    return response, 200, CONTENT_TYPE


if __name__ == '__main__':
    app.run()

