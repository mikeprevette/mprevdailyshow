#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    print("got a request for some webhook")
    # req = request.get_json(silent=True, force=True)
    nothing = "nothing"
    response = makeWebhookResult(nothing)
    print(response)
    r = make_response(response)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(nothing):
    return {
        "speech": 'Cats in the cradle',
        "displayText": 'Cats in the cradle',
        "data": 'google:{"expect_user_response": false,"is_ssml": true}',
        # "contextOut": [],
        "source": "mprevdailyshow"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
