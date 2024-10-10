document.addEventListener('DOMContentLoaded', () => {
    fetchGitHubProjects();
    setupContactForm();
});

async function fetchGitHubProjects() {
    try {
        const response = await fetch('/api/github_projects');
        const projects = await response.json();
        displayProjects(projects);
    } catch (error) {
        console.error('Error fetching GitHub projects:', error);
    }
}

function displayProjects(projects) {
    const projectsContainer = document.getElementById('projects-container');
    projectsContainer.innerHTML = '';

    projects.forEach(project => {
        const projectCard = createProjectCard(project);
        projectsContainer.appendChild(projectCard);
    });
}

function createProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'col-md-6 col-lg-4 mb-4';
    card.innerHTML = `
        <div class="card project-card bg-dark text-light h-100">
            <div class="card-body">
                <h5 class="card-title">${project.name}</h5>
                <p class="card-text">${project.description || 'No description available.'}</p>
                <p class="card-text">
                    <small class="text-muted">
                        <i class="fas fa-star"></i> ${project.stargazers_count} 
                        <i class="fas fa-code-branch ml-2"></i> ${project.forks_count}
                    </small>
                </p>
            </div>
            <div class="card-footer">
                <a href="${project.html_url}" target="_blank" class="btn btn-outline-light btn-sm">View on GitHub</a>
            </div>
        </div>
    `;
    return card;
}

function setupContactForm() {
    const contactForm = document.getElementById('contact-form');
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(contactForm);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                alert('Thank you for your message. I will get back to you soon!');
                contactForm.reset();
            } else {
                throw new Error('Failed to submit the form');
            }
        } catch (error) {
            console.error('Error submitting contact form:', error);
            alert('An error occurred. Please try again later.');
        }
    });
}
