document.addEventListener('DOMContentLoaded', () => {
    const projectsContainer = document.getElementById('projects-container');
    if (projectsContainer) {
        fetchGitHubProjects();
    }

    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        setupContactForm();
    }

    setupDarkModeToggle();
});

async function fetchGitHubProjects() {
    try {
        const response = await fetch('/api/github_projects');
        const projects = await response.json();
        const filteredProjects = filterProjects(projects);
        displayProjects(filteredProjects);
    } catch (error) {
        console.error('Error fetching GitHub projects:', error);
    }
}

function filterProjects(projects) {
    const allowedProjects = [
        'CppND-Route-Planning-Project',
        'EmbeddedC-Game-Dev-Pong-Replica',
        'CppND-System-Monitor',
        'CppND-Memory-Management-Chatbot',
        'CppND-Program-a-Concurrent-Traffic-Simulation',
        'makingEmbeddedSystems'
    ];
    return projects.filter(project => allowedProjects.includes(project.name));
}

function displayProjects(projects) {
    const projectsContainer = document.getElementById('projects-container');
    if (!projectsContainer) {
        return;
    }
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
        <div class="card project-card h-100">
            <div class="card-body">
                <h5 class="card-title">${project.name}</h5>
                <p class="card-text">${project.description || 'No description available.'}</p>
                <p class="card-text">
                    <small class="text-muted">
                        <i class="fas fa-star"></i> ${project.stargazers_count} 
                        <i class="fas fa-code-branch ml-2"></i> ${project.forks_count}
                    </small>
                </p>
                <p class="card-text">
                    <small class="text-muted">Language: ${project.language || 'Not specified'}</small>
                </p>
            </div>
            <div class="card-footer">
                <a href="${project.html_url}" target="_blank" class="btn btn-outline-primary btn-sm">View on GitHub</a>
                <button class="btn btn-outline-secondary btn-sm float-end toggle-details" data-target="details-${project.id}">
                    Show Details
                </button>
            </div>
            <div id="details-${project.id}" class="card-body project-details" style="display: none;">
                <h6>Last Updated: ${new Date(project.updated_at).toLocaleDateString()}</h6>
                <h6>Open Issues: ${project.open_issues_count}</h6>
                <h6>License: ${project.license ? project.license.name : 'Not specified'}</h6>
            </div>
        </div>
    `;

    const toggleButton = card.querySelector('.toggle-details');
    const detailsSection = card.querySelector(`#details-${project.id}`);

    toggleButton.addEventListener('click', () => {
        const isHidden = detailsSection.style.display === 'none';
        detailsSection.style.display = isHidden ? 'block' : 'none';
        toggleButton.textContent = isHidden ? 'Hide Details' : 'Show Details';
    });

    return card;
}

function setupContactForm() {
    const contactForm = document.getElementById('contact-form');
    if (!contactForm) {
        return;
    }
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

function setupDarkModeToggle() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement;
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            if (htmlElement.getAttribute('data-bs-theme') === 'dark') {
                htmlElement.setAttribute('data-bs-theme', 'light');
                darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
                darkModeToggle.classList.remove('btn-outline-light');
                darkModeToggle.classList.add('btn-outline-dark');
            } else {
                htmlElement.setAttribute('data-bs-theme', 'dark');
                darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
                darkModeToggle.classList.remove('btn-outline-dark');
                darkModeToggle.classList.add('btn-outline-light');
            }
        });
    }
}
