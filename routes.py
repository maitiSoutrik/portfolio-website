import os
import requests
from flask import render_template, request, jsonify, redirect, url_for, send_file
from database import db
from models import Contact, BlogPost
from generate_resume import generate_resume

# Custom project descriptions
PROJECT_DETAILS = {
    "CppND-Route-Planning-Project": {
        "description": """An OpenStreetMap route planner implementing the A* search algorithm in C++. 
        This project demonstrates advanced path finding capabilities using real map data. Key features include:
        - Implementation of A* search algorithm for efficient path finding
        - Integration with OpenStreetMap data for real-world navigation
        - Optimized performance using modern C++ features
        - Cross-platform compatibility and easy-to-use interface""",
        "image": "/static/img/projects/osm_map_example.png"
    }
}

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/github_projects')
    def github_projects():
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            app.logger.error('GitHub token not found in environment')
            return jsonify({'error': 'GitHub token not configured'}), 401

        headers = {
            'Authorization': f'Bearer {github_token}',
            'Content-Type': 'application/json',
        }

        # GraphQL query to fetch pinned repositories
        query = """
        {
          user(login: "maitiSoutrik") {
            pinnedItems(first: 6, types: REPOSITORY) {
              nodes {
                ... on Repository {
                  name
                  description
                  url
                  stargazerCount
                  forkCount
                  primaryLanguage {
                    name
                  }
                  updatedAt
                  openIssueCount: issues(states: OPEN) {
                    totalCount
                  }
                  licenseInfo {
                    name
                  }
                }
              }
            }
          }
        }
        """

        try:
            response = requests.post(
                'https://api.github.com/graphql',
                headers=headers,
                json={'query': query},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if 'errors' in data:
                    app.logger.error(f'GitHub GraphQL API error: {data["errors"]}')
                    return jsonify({'error': 'Failed to fetch pinned repositories'}), 500

                # Transform GraphQL response to match the existing frontend expectations
                repos = []
                for repo in data['data']['user']['pinnedItems']['nodes']:
                    transformed_repo = {
                        'name': repo['name'],
                        'description': PROJECT_DETAILS.get(repo['name'], {}).get('description', repo['description']),
                        'html_url': repo['url'],
                        'stargazers_count': repo['stargazerCount'],
                        'forks_count': repo['forkCount'],
                        'language': repo['primaryLanguage']['name'] if repo['primaryLanguage'] else None,
                        'updated_at': repo['updatedAt'],
                        'open_issues_count': repo['openIssueCount']['totalCount'],
                        'license': {'name': repo['licenseInfo']['name']} if repo['licenseInfo'] else None,
                        'full_name': f"maitiSoutrik/{repo['name']}",
                        'image': PROJECT_DETAILS.get(repo['name'], {}).get('image', None)
                    }
                    repos.append(transformed_repo)

                return jsonify(repos)
            else:
                app.logger.error(f'GitHub API error: {response.status_code} - {response.text}')
                return jsonify({'error': f'GitHub API returned status {response.status_code}'}), response.status_code

        except requests.exceptions.RequestException as e:
            app.logger.error(f'Request error: {str(e)}')
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