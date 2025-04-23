
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
    
    return render(request, 'article/article_list.html', {
        'articles': articles['results']
    })

def article_detail(request, pk):
    """
    View to fetch and display the details of a specific article.
    """
    try:
        article = api_articles.get_article_by_id(request, pk)
        if not article:
            messages.error(request, 'Article not found.')
            return render(request, 'article/article_detail.html', {'article': None})
    except requests.RequestException as e:
        messages.error(request, 'Failed to fetch article details. Please try again later.')
        return render(request, 'article/article_detail.html', {'article': None})
    
    return render(request, 'article/article_detail.html', {
        'article': article
    })