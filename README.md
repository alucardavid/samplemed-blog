# Blog SampleMed

A Django-based blog platform with a REST API backend and server-side rendered frontend.

## Features

- REST API with JWT authentication
- Server-side rendered frontend
- Article management with keywords and comments
- User registration and authentication
- Swagger/OpenAPI documentation
- Caching system
- Custom error handling
- Test coverage

## Tech Stack

- Python 3.12
- Django 5.2
- Django REST Framework 3.16
- JWT Authentication
- Bootstrap 5
- SQLite

## Project Structure

```
blog_samplemed/
├── apps/
│   ├── api/             # REST API implementation
│   │   ├── models/      # Database models
│   │   ├── serializers/ # DRF serializers
│   │   ├── views/       # API views
│   │   └── urls.py      # API URL routing
│   ├── core/            # Core business logic
│   │   ├── services/    # Business services
│   │   └── exceptions/  # Custom exceptions
│   └── frontend/        # Server-side rendered frontend
│       ├── templates/   # HTML templates
│       ├── views/       # Frontend views
│       └── services/    # Frontend services
└── blog_samplemed/      # Project settings
```

## API Endpoints

### Authentication
```
POST /api/v1/token/         # Obtain JWT token
POST /api/v1/token/refresh/ # Refresh JWT token
```

### Users
```
GET    /api/v1/users/       # List users
POST   /api/v1/users/       # Create user
GET    /api/v1/users/{id}/  # Get user details
PUT    /api/v1/users/{id}/  # Update user
DELETE /api/v1/users/{id}/  # Delete user
```

### Articles
```
GET    /api/v1/articles/                    # List articles
POST   /api/v1/articles/                    # Create article
GET    /api/v1/articles/{id}/               # Get article details
PUT    /api/v1/articles/{id}/               # Update article
DELETE /api/v1/articles/{id}/               # Delete article
GET    /api/v1/articles/author/{author_id}/ # Get articles by author
```

### Comments
```
GET    /api/v1/comments/       # List comments
POST   /api/v1/comments/       # Create comment
GET    /api/v1/comments/{id}/  # Get comment details
PUT    /api/v1/comments/{id}/  # Update comment
DELETE /api/v1/comments/{id}/  # Delete comment
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alucardavid/samplemed-blog.git
cd samplemed-blog
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=1
CORS_ALLOWED_ORIGINS=http://localhost:8000
API_URL=http://localhost:8000
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Usage Examples

### Creating an Article via API

```python
import requests

# Login and get token
token_response = requests.post('http://localhost:8000/api/v1/token/', {
    'username': 'your-username',
    'password': 'your-password'
})
token = token_response.json()['access']

# Create article
headers = {'Authorization': f'Bearer {token}'}
article_data = {
    'title': 'My First Article',
    'subtitle': 'An interesting subtitle',
    'content': 'Article content goes here...',
    'type': 1,  # Published
    'status': 1,  # Public
    'keywords': ['python', 'django']
}

response = requests.post(
    'http://localhost:8000/api/v1/articles/',
    json=article_data,
    headers=headers
)
```

### Frontend Templates

The frontend uses Bootstrap 5 for styling. Example article list template:

```html
{% extends 'shared/base.html' %}
{% block content %}
<div class="row">
    <div class="col-12">
        <h2>Articles</h2>
        {% for article in articles %}
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">{{ article.title }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">
                        {{ article.subtitle }}
                    </h6>
                    <p class="card-text">
                        {{ article.content|truncatechars:150 }}
                    </p>
                    <a href="{% url 'frontend:article_detail' pk=article.id %}" 
                       class="btn btn-primary">
                        Read More
                    </a>
                </div>
            </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

## Testing

Run the test suite:

```bash
python manage.py test
```

Example test case:

```python
from apps.api.tests.base import BaseAPITestCase
from django.urls import reverse
from rest_framework import status

class ArticleAPITests(BaseAPITestCase):
    def test_create_article(self):
        self.authenticate()
        url = reverse('api:v1:article-list')
        data = {
            'title': 'Test Article',
            'subtitle': 'Test Subtitle',
            'content': 'Test Content',
            'type': 0,
            'status': 0,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

## API Documentation

The API documentation is available at:

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

