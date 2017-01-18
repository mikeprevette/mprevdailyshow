import urllib2
import json
import os
import xml.etree.ElementTree as ET

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

#Globals 

googleSpecs = 'google:{"expect_user_response": false,"is_ssml": true}'


# REMOVE THE FOLLOWING FOR THE DAILY SHOW 
@app.route('/subway', methods=['POST'])
def subway():
    postData = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(postData, indent=4))
    trainStatus = picktrain(postData)
    trainStatus = json.dumps(trainStatus, indent=4)
    x = make_response(trainStatus)
    x.headers['Content-Type'] = 'application/json'   
    return x

def picktrain(req):
    if req.get("result").get("action") != "checkTrainStatus":
      return {}
    myTrainLine = req.get("result").get("parameters").get("trainLine")
    print("my train " + myTrainLine)
    myLineStatus = getMTA(myTrainLine)
    speech = "<speak>The " + myTrainLine + " train currently has " + myLineStatus + "</speak>"
    return {
        "speech": speech,
        "displayText": speech,
        "data": googleSpecs,
        "source": "mprevSubway"
    }


def getMTA(myTrainLine):
    mtaURL = 'http://web.mta.info/status/serviceStatus.txt'
    result = urllib2.urlopen(mtaURL).read()
    tree = ET.ElementTree(result)
    root = tree.getroot()
    myLine = "null"
    rootElement = ET.fromstring(root)
    rootStr = rootElement.tag
    for line in rootElement.find('subway').iter('line'):
        lineName = line.find('name').text
        lineStatus = line.find('status').text
        print(lineName, lineStatus)
        if myTrainLine.upper() in lineName: 
            myLine = lineStatus
            break
    return myLine


@app.route('/tdswebhook', methods=['POST'])
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
    result = urllib2.urlopen(baseURL).read()
    data = json.loads(result)
    #print(data)
    res = makeWebhookResult(data)
    return res




def makeWebhookResult(data):
    #print("Making Webhook Result")
   
    tdsURL = data.get('streamUrl')
    tdsDate = data.get('updateDate')
    tdsDate = tdsDate = tdsDate[:-15]
    #print(tdsDate)
    if tdsURL is None:
        return {}

    speech = "<speak>from <say-as interpret-as='date' format='yyyymmdd' detail='2'>" + tdsDate + "</say-as><audio src='" + tdsURL + "'>The Latest Daily show</audio></speak>"
    #print("Response:")
    #print(speech)

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