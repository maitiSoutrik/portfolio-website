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
    new_contact = Contact(
        name=data['name'],
        email=data['email'],
        message=data['message']
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'message': 'Contact form submitted successfully'}), 201

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
