from flask import Flask, render_template, jsonify, request
from datetime import datetime
import requests
import os
import json
import logging

app = Flask(__name__)

DEFAULT_REPO = os.getenv('GITHUB_REPO', 'JB-700/5MCSI_Metriques')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', None)

def get_commits_from_github(repo_fullname=5MCSI_Metriques, per_page=100, max_pages=3):
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    commits = []
    for page in range(1, max_pages + 1):
        url = f'https://api.github.com/repos/JB-700/5MCSI_Metriques/commits'
        params = {'per_page': per_page, 'page': page}
        try:
            r = requests.get(url, headers=headers, params=params, timeout=10)
        except Exception as e:
            logging.exception("Erreur requête GitHub: %s", e)
            break
        if r.status_code != 200:
            logging.warning("GitHub API returned %s for %s (page %d): %s", r.status_code, repo_fullname, page, r.text[:200])
            break
        page_data = r.json()
        if not page_data:
            break
        commits.extend(page_data)
        if len(page_data) < per_page:
            break
    return commits

def aggregate_commits_per_minute(commits):
    counts = [0] * 60
    for c in commits:
        date_str = None
        try:
            date_str = c.get('commit', {}).get('author', {}).get('date')
        except Exception:
            date_str = None
        if not date_str:
            continue
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = dt.minute
            counts[minute] += 1
        except Exception:
            continue
    return counts

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
    except Exception:
        return jsonify({'error': 'format invalide, attendu YYYY-MM-DDTHH:MM:SSZ'}), 400

@app.route('/commits/data')
def commits_data():
    repo = request.args.get('repo', DEFAULT_REPO)
    try:
        per_page = int(request.args.get('per_page', 100))
    except:
        per_page = 100
    try:
        pages = int(request.args.get('pages', 2))
    except:
        pages = 2
    commits = get_commits_from_github(repo_fullname=repo, per_page=per_page, max_pages=pages)
    counts = aggregate_commits_per_minute(commits)
    labels = [f"{i:02d}" for i in range(60)]
    total = sum(counts)
    return jsonify({
        'repo': repo,
        'labels': labels,
        'counts': counts,
        'total_commits': total,
        'fetched_commits': len(commits)
    })

@app.route('/commits/')
def commits_page():
    return render_template('commits.html')

if __name__ == '__main__':
    app.run(debug=True)
