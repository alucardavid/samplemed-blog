from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
import requests


def index(request):
    # Url apis to fetch articles
    api_url = f'{settings.API_URL}/api/v1/articles/'
    headers = {}
    
    # If the user is authenticated, add the JWT token to the headers
    if request.user.is_authenticated:
        token = request.session.get('jwt_token')
        if token:
            headers['Authorization'] = f'Bearer {token}'
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status() # Raise an error for bad responses (4xx and 5xx)
        articles = response.json()
    except requests.RequestException as e:
        messages.error(request, 'Failed to fetch articles. Please try again later.')
        articles = {'results': []} 

    return render(request, 'home/index.html', {
        'articles': articles.get('results', [])
    })