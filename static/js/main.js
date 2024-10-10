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
        displayProjects(projects);
    } catch (error) {
        console.error('Error fetching GitHub projects:', error);
    }
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
            </div>
            <div class="card-footer">
                <a href="${project.html_url}" target="_blank" class="btn btn-outline-primary btn-sm">View on GitHub</a>
            </div>
        </div>
    `;
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
