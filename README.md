# weather-api
An api using python-flask to get latest weather data by calling exteranal <a href = "https://www.weather.gov/documentation/services-web-api">api</a> of national weather service.
<br> <br>
<strong>Required python modules:</strong>
<ul> 
  <li>Flask </li>
  <li>requests </li>
  <li>json </li>
</ul>
<br>

Run : <br>
<code> $ python api.py </code> <br>

Open browser, visit following urls :  <br>
<dl>
  <dt><strong>http://127.0.0.1:5000/</strong></dt>
  <dd> - home page
  <dt><strong>http://127.0.0.1:5000/metar/{any random text here}</strong></dt>
  <dd>- To check working of api route</dd>
   <dt><strong>http://127.0.0.1:5000/metar/info/{station code here}</strong></dt>
  <dd>- To get latest weather data of a station</dd>
</dl> <br>

Station codes : <a href = "https://www.weather.gov/arh/stationlist">List</a>
