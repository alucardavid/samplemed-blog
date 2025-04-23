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