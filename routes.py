import os
import requests
from flask import render_template, request, jsonify, redirect, url_for, send_file
from models import Contact, BlogPost
from database import db
from generate_resume import generate_resume

# Generate the resume PDF when the application starts
generate_resume()

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/github_projects')
    def github_projects():
        username = 'maitiSoutrik'
        url = f'https://api.github.com/users/{username}/repos'
        headers = {}
        if github_token := os.environ.get("GITHUB_TOKEN"):
            headers['Authorization'] = f'token {github_token}'
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                projects = response.json()
                return jsonify(projects)
            else:
                return jsonify({'error': f'GitHub API returned status {response.status_code}'}), response.status_code
        except Exception as e:
            return jsonify({'error': str(e)}), 500

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
        experiences = [
            {
                'title': 'Senior Embedded Software Engineer',
                'company': 'TechCorp',
                'period': 'Jan 2020 - Present',
                'description': 'Leading embedded software development for IoT devices.',
                'responsibilities': [
                    'Architecting and implementing firmware for various IoT devices',
                    'Optimizing power consumption and performance of embedded systems',
                    'Mentoring junior engineers and leading cross-functional teams'
                ],
                'technologies': 'C, C++, FreeRTOS, ARM Cortex-M, Bluetooth Low Energy, Zigbee'
            },
            {
                'title': 'Embedded Software Engineer',
                'company': 'InnovativeSystems',
                'period': 'Jun 2017 - Dec 2019',
                'description': 'Developed firmware for automotive control systems.',
                'responsibilities': [
                    'Designing and implementing real-time software for automotive ECUs',
                    'Integrating and testing CAN, LIN, and FlexRay communication protocols',
                    'Collaborating with hardware engineers to optimize system performance'
                ],
                'technologies': 'C, AUTOSAR, MISRA C, Vector CANoe, ETAS ASCET'
            },
            {
                'title': 'Junior Software Developer',
                'company': 'StartupTech',
                'period': 'Sep 2015 - May 2017',
                'description': 'Worked on embedded Linux systems for smart home devices.',
                'responsibilities': [
                    'Developing and maintaining Linux device drivers',
                    'Implementing user-space applications for smart home control',
                    'Assisting in the design and implementation of OTA update mechanisms'
                ],
                'technologies': 'C, Python, Embedded Linux, Yocto Project, Git, Jenkins'
            }
        ]
        return render_template('timeline.html', experiences=experiences)

    @app.route('/download_resume')
    def download_resume():
        return send_file('static/resume.pdf', as_attachment=True)
