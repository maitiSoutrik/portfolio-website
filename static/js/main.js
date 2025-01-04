document.addEventListener('DOMContentLoaded', () => {
    const projectsContainer = document.getElementById('projects-container');
    if (projectsContainer) {
        fetchGitHubProjects();
    } else {
        console.error('Projects container not found');
    }

    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        setupContactForm();
    } else {
        console.error('Contact form not found');
    }

    setupDarkModeToggle();
    setupTimeline();
});

async function fetchGitHubProjects() {
    try {
        const response = await fetch('/api/github_projects');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const projects = await response.json();
        const projectsWithReadme = await Promise.all(projects.map(fetchReadmeContent));
        displayProjects(projectsWithReadme);
    } catch (error) {
        console.error('Error fetching GitHub projects:', error);
        const projectsContainer = document.getElementById('projects-container');
        if (projectsContainer) {
            projectsContainer.innerHTML = '<div class="alert alert-danger">Failed to load projects. Please try again later.</div>';
        }
    }
}

async function fetchReadmeContent(project) {
    try {
        const readmeResponse = await fetch(`https://api.github.com/repos/${project.full_name}/readme`);
        if (readmeResponse.ok) {
            const readmeData = await readmeResponse.json();
            project.readmeContent = atob(readmeData.content);
        }
    } catch (error) {
        console.error(`Error fetching README for ${project.name}:`, error);
        project.readmeContent = '';
    }
    return project;
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

    // Use custom project image if available, fallback to README image or placeholder
    const imageUrl = project.image || extractImageFromReadme(project.readmeContent) || '/static/img/placeholder.svg';

    card.innerHTML = `
        <div class="card project-card h-100">
            <img src="${imageUrl}" class="card-img-top" alt="${project.friendly_name || project.name} image" onerror="this.src='/static/img/placeholder.svg'">
            <div class="card-body">
                <h5 class="card-title">${project.friendly_name || project.name}</h5>
                <p class="card-text">${project.description || 'No description available.'}</p>
                <p class="card-text">
                    <small class="text-muted">Built with ${project.language || 'Various Technologies'}</small>
                </p>
                <a href="${project.html_url}" target="_blank" class="btn btn-primary w-100 mb-2">
                    <i class="fab fa-github"></i> View Project on GitHub
                </a>
            </div>
            <div class="card-footer">
                <button class="btn btn-outline-secondary btn-sm w-100 toggle-details" data-target="details-${project.id}">
                    Show Technical Details
                </button>
            </div>
            <div id="details-${project.id}" class="card-body project-details" style="display: none;">
                <h6>Last Updated: ${new Date(project.updated_at).toLocaleDateString()}</h6>
                <h6>License: ${project.license ? project.license.name : 'Not specified'}</h6>
                <p class="text-muted small">Repository: ${project.name}</p>
            </div>
        </div>
    `;

    const toggleButton = card.querySelector('.toggle-details');
    const detailsSection = card.querySelector(`#details-${project.id}`);

    toggleButton.addEventListener('click', () => {
        const isHidden = detailsSection.style.display === 'none';
        detailsSection.style.display = isHidden ? 'block' : 'none';
        toggleButton.textContent = isHidden ? 'Hide Technical Details' : 'Show Technical Details';
    });

    return card;
}

function extractImageFromReadme(readmeContent) {
    const imageRegex = /!\[.*?\]\((.*?)\)/;
    const match = readmeContent.match(imageRegex);
    return match ? match[1] : null;
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

function setupTimeline() {
    const timelineItems = document.querySelectorAll('.timeline-item');
    const toggleButtons = document.querySelectorAll('.toggle-details');
    
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    timelineItems.forEach(item => {
        observer.observe(item);
    });

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);
            if (targetElement.classList.contains('show')) {
                targetElement.classList.remove('show');
                button.textContent = 'Show Details';
            } else {
                targetElement.classList.add('show');
                button.textContent = 'Hide Details';
            }
        });
    });

    const timelineNavLinks = document.querySelectorAll('.timeline-nav a');
    timelineNavLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });
}