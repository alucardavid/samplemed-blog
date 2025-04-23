from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
import requests

from apps.frontend.services import api_articles


def index(request):
    """Render the home page with articles."""
    try:
        articles = api_articles.get_articles()
        if not articles:
            messages.error(request, 'No articles found.')
            articles = {'results': []}  # Default to an empty list if no articles found
    except requests.RequestException as e:
        messages.error(request, 'Failed to fetch articles. Please try again later.')
        articles = {'results': []} 

    return render(request, 'home/index.html', {
        'articles': articles.get('results', [])
    })