# @Date:   2020-10-15T20:09:52+05:30
# @Last modified time: 2020-10-16T20:25:52+05:30
# @Developer: nilesh8757



# import necessary libraries and functions
from flask import Flask, render_template, jsonify, request
import requests, json
import redis_connector as rc

# creating a Flask app
app = Flask(__name__, template_folder='template')
c = rc.Cache()

def get_data_in_format(scode, response):
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
	return parsed

def set_cache(scode, response):
	parsedData = get_data_in_format(scode, response)
	c.cache(scode, parsedData)
	return parsedData

# visit : http://127.0.0.1:5000/
@app.route('/', methods = ['GET'])
def root():
	if(request.method == 'GET'):
		return render_template('/index.html')

#visit to test route: http://127.0.0.1:5000/metar/<random text here>
@app.route('/metar/<string:data>', methods = ['GET', 'POST'])
def home(data):
	if(request.method == 'GET'):
		return jsonify({'data': data})


#get weather info at : http://127.0.0.1:5000/metar/info/<station code>/nocache
#if nochae == 1, fetch fresh result, else first look for data in cache
@app.route('/metar/info/<string:scode>/<int:nocache>', methods = ['GET', 'POST'])
def disp(scode, nocache):
    url = "https://api.weather.gov/stations/" + scode + "/observations/latest"
    if nocache == 1:
        response = requests.get(url)
        if(not response.ok):
            return render_template('/error.html')
        else:
            parsedData = set_cache(scode, response)
            return jsonify({'data': parsedData})
    else:
	    data_from_cahce = c.get(scode)
	    if data_from_cahce is None:
		    response = requests.get(url)
		    if(not response.ok):
			    return render_template('/error.html')
		    else:
			    parsedData = set_cache(scode, response)
			    return jsonify({'data': parsedData})
	    else:
		    parsedData = data_from_cahce.decode('utf-8')
		    return jsonify({'data': parsedData})


# driver function
if __name__ == '__main__':
	app.run(debug = True)
