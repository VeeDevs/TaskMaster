#TaskMaster Django Capstone Project

## Project Description

TaskMaster is a feature-rich task management application built using Django. It serves as the capstone project for a comprehensive software engineering course. The application allows users to create, update, and manage their tasks efficiently. Designed with a focus on simplicity and functionality, TaskMaster helps users stay organized and productive. The project showcases expertise in Django, Python, HTML, CSS, and Bootstrap, demonstrating skills in web development and deployment.

## Features

- User authentication and authorization
- CRUD operations for various models (e.g., articles, comments, profiles)
- Integration with third-party APIs (e.g., social media, weather)
- Responsive and mobile-friendly user interface
- Automated testing and continuous integration

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Django 3.2 or higher
- A virtual environment management tool (e.g., virtualenv, pipenv, conda)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/django-capstone-project.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd django-capstone-project
    ```

3. **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

4. **Install the project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Apply the database migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Start the development server:**

    ```bash
    python manage.py runserver
    ```

7. **Open your web browser and navigate to** [http://localhost:8000](http://localhost:8000) **to access the application.**

### Using Docker

1. **Build the Docker image:**

    ```bash
    docker build -t django-capstone-project .
    ```

2. **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 django-capstone-project
    ```

3. **Open your web browser and navigate to** [http://localhost:8000](http://localhost:8000) **to access the application.**

### Acquiring Sensitive Files and Tokens

Some parts of the application may require sensitive files or tokens (e.g., API keys, environment variables). To acquire these, please contact the project maintainers.

## Documentation

The documentation for this Django Capstone Project is available in the `docs` folder. You can generate the HTML documentation by running the following command:

```bash
sphinx-build -b html . docs
