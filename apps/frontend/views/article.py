
from django.shortcuts import render, redirect
from django.conf import settings
from apps.frontend.forms import ArticleCreateForm
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

def article_create(request):
    """
    View to handle the creation of a new article.
    """
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST)
        if form.is_valid():
            try:
                article = api_articles.create_article(request, form.cleaned_data)
                if not article:
                    messages.error(request, 'Failed to create article. Please try again later.')
                    return redirect('frontend:article_create')
                messages.success(request, 'Article created successfully.')
                return redirect('frontend:article_detail', pk=article['id'])
            except requests.RequestException as e:
                messages.error(request, 'Failed to create article. Please try again later.')
    else:
        form = ArticleCreateForm()

    return render(request, 'article/article_create.html', {'form': form})