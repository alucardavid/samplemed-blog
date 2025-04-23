from django.conf import settings
import requests


def get_articles():
    # Url apis to fetch articles
    api_url = f'{settings.API_URL}/api/v1/articles/'
    headers = {
        'Content-Type': 'application/json'
    }

    # Fetch articles from the API
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        articles = response.json()
        return articles
    
def get_article_by_id(request, article_id):
    # Url apis to fetch articles
    api_url = f'{settings.API_URL}/api/v1/articles/{article_id}/'
    headers = {
        'Content-Type': 'application/json'
    }

    # Fetch articles from the API
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        article = response.json()
        return article
    
def create_comment(request, article_id, comment):
    # Url apis to fetch articles
    api_url = f'{settings.API_URL}/api/v1/comments/'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {request.session.get('jwt_token')}'
    }

    payload = {
        'content': comment,
        'article': article_id	
    }

    # Fetch articles from the API
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 201:
        comment = response.json()
        return comment
    
def create_article(request, article):
    # Url apis to fetch articles
    api_url = f'{settings.API_URL}/api/v1/articles/'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {request.session.get('jwt_token')}'
    }

    payload = {
        'title': article['title'],
        'subtitle': article['subtitle'],
        'content': article['content'],
        'type': article['type'],
        'status': article['status'],
        'keywords': article['keywords'],
    }

    # Fetch articles from the API
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 201:
        article = response.json()
        return article