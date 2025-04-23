
from django.shortcuts import render
from django.conf import settings
from apps.frontend.services import api_articles
from django.contrib import messages
import requests

def article_list(request):
    """
    View to fetch and display a list of articles from the API.
    """
    try:
        articles = api_articles.get_articles()
        if not articles:
            messages.error(request, 'No articles found.')
            articles = {'results': []}  # Default to an empty list if no articles found
    except requests.RequestException as e:
        messages.error(request, 'Failed to fetch articles. Please try again later.')
        articles = {'results': []} 
    
    return render(request, 'articles/articles_list.html', {
        'articles': articles['results']
    })