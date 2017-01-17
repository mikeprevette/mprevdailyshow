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
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    #print("Process Request")
    if req.get("result").get("action") != "latestDailyShow":
      return {}
    baseURL = "https://api.cc.com/feeds/alexa/tdsnews/v1_0_0"
    result = urllib.urlopen(baseURL).read()
    data = json.loads(result)
    #print(data)
    res = makeWebhookResult(data)
    return res




def makeWebhookResult(data):
    #print("Making Webhook Result")
   
    tdsURL = data.get('streamUrl')
    if tdsURL is None:
        return {}

    speech = "<speak><audio src='" + tdsURL + "'>The Latest Daily show</audio></speak>"
    #print("Response:")
    #print(speech)

    googleSpecs = 'google:{"expect_user_response": false,"is_ssml": true}'

    return {
        "speech": speech,
        "displayText": speech,
        "data": googleSpecs,
        # "contextOut": [],
        "source": "mprevDailyShow"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')