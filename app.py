# import flask dependencies
from flask import Flask, request, make_response, jsonify

import requests
import json

URL = "https://stallingsnet.nl/api/1/parkingcount/utrecht"
r = requests.get(url = URL)

rawdata = r.json()
dumpdata = json.dumps(rawdata)
usabledata = json.loads(dumpdata)



# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('action')
    inputlocation = req.get('queryResult').get('parameters').get("Location")
    correctornot = False
    while correctornot == False:
        for x in usabledata:
            loc = x['facilityName']
            if loc.lower() == inputlocation.lower():
                data = x
                correctornot = True
        if correctornot == False:
            return {'fulfillmentText': "Whoops, die fietsenstalling kan niet worden gevonden. Probeer opnieuw "}

    return{'fulfillmentText': "In de fietsenstalling " + data['facilityName'] + " zijn momenteel nog " + str(
        data['freePlaces']) + " plaatsen van de " + str(data['totalPlaces']) + " totale plaatsen beschikbaar."}
    # return a fulfillment response

    return {'fulfillmentText': 'error'}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()