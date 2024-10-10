import requests
from flask import render_template, request, jsonify
from app import app, db
from models import Contact

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/github_projects')
def github_projects():
    username = 'maitiSoutrik'
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    if response.status_code == 200:
        projects = response.json()
        return jsonify(projects)
    else:
        return jsonify({'error': 'Unable to fetch GitHub projects'}), 500

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    new_contact = Contact(
        name=data['name'],
        email=data['email'],
        message=data['message']
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'message': 'Contact form submitted successfully'}), 201
