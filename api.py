# @Date:   2020-10-15T20:09:52+05:30
# @Last modified time: 2020-10-15T21:50:01+05:30
# @Developer: nilesh8757



# import necessary libraries and functions
from flask import Flask, render_template, jsonify, request
import requests, json

# creating a Flask app
app = Flask(__name__, template_folder='template')

# visit : http://127.0.0.1:5000/
@app.route('/', methods = ['GET'])
def root():
	if(request.method == 'GET'):
		return render_template('/index.html')

#visit to test route: http://127.0.0.1:5000/metar/<any random text here>
@app.route('/metar/<string:data>', methods = ['GET', 'POST'])
def home(data):
	if(request.method == 'GET'):
		return jsonify({'data': data})


#get weather info at : http://127.0.0.1:5000/metar/info/<station code here>
@app.route('/metar/info/<string:scode>', methods = ['GET'])
def disp(scode):
    url = "https://api.weather.gov/stations/" + scode + "/observations/latest"
    response = requests.get(url)
    if(response.status_code != 200):
        return render_template('/error.html')
    else:
        res = response.json()
        data = {
            "station" : scode,
            "coordinates": res["geometry"]["coordinates"],
            "last_observation": res["properties"]["timestamp"],
            "temperature": str(res["properties"]["temperature"]["value"]) + " C",
            "wind direction": str(res["properties"]["windDirection"]["value"]) + " degree",
            "wind speed": str(res["properties"]["windSpeed"]["value"]) + " kmph",
            "message" : res["properties"]["rawMessage"]
        }

        data = json.dumps(data, sort_keys = True, indent = 3)
        parsed = json.loads(data)
        return jsonify({'data': parsed})

# driver function
if __name__ == '__main__':
	app.run(debug = True)
