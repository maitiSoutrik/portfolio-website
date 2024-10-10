import requests
from flask import render_template, request, jsonify, redirect, url_for
from app import app, db
from models import Contact, BlogPost

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
    if data:
        new_contact = Contact(
            name=data.get('name'),
            email=data.get('email'),
            message=data.get('message')
        )
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({'message': 'Contact form submitted successfully'}), 201
    return jsonify({'error': 'Invalid data'}), 400

@app.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog_post.html', post=post)

@app.route('/blog/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        new_post = BlogPost(
            title=request.form['title'],
            content=request.form['content']
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog'))
    return render_template('new_post.html')

@app.route('/timeline')
def timeline():
    # For now, we'll use hardcoded data. In a real application, this would come from a database.
    experiences = [
        {
            'title': 'Senior Embedded Software Engineer',
            'company': 'TechCorp',
            'period': 'Jan 2020 - Present',
            'description': 'Leading embedded software development for IoT devices.'
        },
        {
            'title': 'Embedded Software Engineer',
            'company': 'InnovativeSystems',
            'period': 'Jun 2017 - Dec 2019',
            'description': 'Developed firmware for automotive control systems.'
        },
        {
            'title': 'Junior Software Developer',
            'company': 'StartupTech',
            'period': 'Sep 2015 - May 2017',
            'description': 'Worked on embedded Linux systems for smart home devices.'
        }
    ]
    return render_template('timeline.html', experiences=experiences)
