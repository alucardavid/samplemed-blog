from django.contrib.auth.models import User
from django.conf import settings
import requests


def register_user(user: User) -> dict:
    """
    Register a new user with the given username and password.

    Parameters:
        - user (User): The user object containing the username and password.
        
    """
    
    # Url apis to fetch articles
    api_url = f'{settings.API_URL}/api/v1/users/'
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        'username': user.username,
        'password': user.password,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code == 201:
        return response.json()
    else:
        return {'error': response.json()}
    

def login_user(username: str, password: str) -> dict:
    """
    Log in a user with the given username and password.

    Parameters:
        - username (str): The username of the user.
        - password (str): The password of the user.
        
    """
    
    # Url apis to fetch articles
    api_url = f'{settings.API_URL}/api/v1/token/'
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        'username': username,
        'password': password,
    }

    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.json()}