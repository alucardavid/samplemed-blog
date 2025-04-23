
from django.shortcuts import render, redirect
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

def comment_create(request, pk):
    """
    View to handle the creation of a comment on an article.
    """
    if request.method == 'POST':
        comment = request.POST.get('comment-content')
        if not comment:
            messages.error(request, 'Comment cannot be empty.')
            return redirect('article_detail', pk=pk)
        
        try:
            api_articles.create_comment(request, pk, comment)
            messages.success(request, 'Comment added successfully.')
        except requests.RequestException as e:
            messages.error(request, 'Failed to add comment. Please try again later.')
    
    return redirect('frontend:article_detail', pk=pk)