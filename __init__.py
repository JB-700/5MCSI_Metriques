from flask import Flask, render_template, jsonify
from urllib.request import urlopen
import json
import logging

app = Flask(__name__)

# Définir une fonction utilitaire pour récupérer et formater les données
def fetch_tawarano_data():
    """
    Récupère les données depuis l'API OpenWeather (exemple) et renvoie une liste
    de dicts de la forme { 'Jour': <unix_seconds>, 'temp': <celsius_float> }.
    """
    try:
        response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx', timeout=10)
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
    except Exception as e:
        logging.exception("Erreur lors de la récupération des données OpenWeather : %s", e)
        return []  # retourne une liste vide en cas d'erreur

    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        # Par sécurité vérifier que main/temp existe
        main_obj = list_element.get('main', {})
        if dt_value is None or 'temp' not in main_obj:
            continue
        temp_kelvin = main_obj.get('temp')
        temp_celsius = temp_kelvin - 273.15  # Conversion Kelvin -> °C
        results.append({'Jour': dt_value, 'temp': temp_celsius})
    return results

@app.route('/')
def index():
    return render_template('hello.html')

@app.route('/contact/')
def contact():
    return "<h2>Ma page de contact</h2>"

@app.route('/tawarano/')
def meteo():
    results = fetch_tawarano_data()
    return jsonify(results=results)

@app.route('/histogramme/')
def histogramme():
    results = fetch_tawarano_data()
    # Sérialiser en JSON string pour l'injecter proprement dans le template
    results_json = json.dumps(results)
    return render_template('histogramme.html', results_json=results_json)

@app.route('/rapport/')
def mongraphique():
    return render_template('graphique.html')

if __name__ == "__main__":
    # debug True pour le développement ; change selon le contexte de déploiement
    app.run(debug=True)
