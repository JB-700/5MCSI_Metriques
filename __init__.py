# app.py
from flask import Flask, render_template, jsonify
from urllib.request import urlopen
import json
import logging

app = Flask(__name__)

def fetch_tawarano_data():
    """
    Récupère et formate les données depuis l'API d'exemple OpenWeather.
    Renvoie une liste de dicts : {'Jour': <unix_seconds>, 'temp': <celsius>}
    """
    try:
        response = urlopen(
            'https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx',
            timeout=10
        )
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
    except Exception:
        logging.exception("Erreur lors de la récupération des données OpenWeather")
        return []

    results = []
    for item in json_content.get('list', []):
        dt_value = item.get('dt')
        main_obj = item.get('main', {})
        if dt_value is None or 'temp' not in main_obj:
            continue
        temp_celsius = main_obj.get('temp') - 273.15
        results.append({'Jour': dt_value, 'temp': temp_celsius})
    return results

@app.route('/')
def index():
    return render_template('hello.html')


@app.route('/contact/')
def contact_page():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    results = fetch_tawarano_data()
    return jsonify(results=results)

@app.route('/histogramme/')
def histogramme():
    
    results = fetch_tawarano_data()
    results_json = json.dumps(results)
    return render_template('histogramme.html', results_json=results_json)

@app.route('/rapport/')
def mongraphique():
    return render_template('graphique.html')

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

if __name__ == "__main__":
    app.run(debug=True)
