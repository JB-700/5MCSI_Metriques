from flask import Flask, render_template, jsonify
import json
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

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

@app.route('/histogramme/')



def histogramme():
    results = fetch_tawarano_data()
    results_json = json.dumps(results)
    return render_template('histogramme.html', results_json=results_json)

@app.route('/commits/')
def commits():
    req = Request('https://api.github.com/repos/JB-700/5MCSI_Metriques/commits', headers={'User-Agent': 'python-urllib'})
    try:
        response = urlopen(req, timeout=10)
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
    except (HTTPError, URLError, TimeoutError):
        json_content = []

    commits_per_minute = {i: 0 for i in range(60)}
    for commit in json_content:
        date_string = commit.get('commit', {}).get('author', {}).get('date')
        if not date_string:
            continue
        try:
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        except Exception:
            continue
        minutes = date_object.minute
        commits_per_minute[minutes] += 1

    labels = [f"{i:02d}" for i in range(60)]
    counts = [commits_per_minute[i] for i in range(60)]
    data_payload = {
        'repo': 'JB-700/5MCSI_Metriques',
        'labels': labels,
        'counts': counts,
        'total_commits': sum(counts),
        'fetched_commits': len(json_content)
    }
    results_json = json.dumps(data_payload)
    return render_template("commits.html", results_json=results_json)

@app.route("/commits-graph/")
def commits_graph():
    return render_template("commits.html")

if __name__ == "__main__":
    app.run(debug=True)
