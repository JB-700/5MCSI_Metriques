from flask import Flask, render_template, jsonify
import json
from datetime import datetime
from urllib.request import urlopen

app = Flask(__name__)

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/commits/')
def commits():
    response = urlopen('https://api.github.com/repos/JB-700/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    commits_per_minute = {}
    for i in range(60):
        commits_per_minute[i] = 0
    for commit in json_content:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        commits_per_minute[minutes] += 1
    results = []
    for minute, count in commits_per_minute.items():
        results.append({'minute': minute, 'count': count})
    return jsonify(results=results)

@app.route("/commits-graph/")
def commits_graph():
    return render_template("commits.html")

if __name__ == "__main__":
    app.run(debug=True)
