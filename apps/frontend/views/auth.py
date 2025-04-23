from django.contrib.messages import get_messages
from django.conf import settings
from django.shortcuts import redirect, render
from apps.frontend.forms import LoginForm, RegisterForm
from apps.frontend.services import api_auth as auth_service
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def register(request):
    """
        View to handle user registration.
        It uses a custom form to collect user data and sends it to the API for registration.
    """

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # call api to register user
            api_response = auth_service.register_user(user)

            if 'error' not in api_response:
                # Registered successfully, redirect to login page
                user_login = authenticate(
                    request, username=user.username, password=form.cleaned_data['password']
                )

                # If user is authenticated, log them in
                if user_login is not None:
                    auth_login(request, user_login)                

                # Store JWT token in session
                request.session['jwt_token'] = api_response['access']

                # Redirect to a success page or render a success template
                return render(request, 'auth/login_success.html', {
                    'token': api_response['access']
                })
            else:
                form.add_error(None, api_response.get('error', 'Erro ao registrar usuário.'))
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})

def logout(request):
    """
        View to handle user logout.
        It clears the session and redirects to the login page.
    """
    # Clear the session
    auth_logout(request)    
    
    # Redirect to the login page or any other page
    return redirect('frontend:index')

def login(request):
    """
        View to handle user login.
        It authenticates the user and redirects to the dashboard if successful.
    """
    if request.user.is_authenticated:
        return redirect('frontend:index')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # call api to login user
            api_response = auth_service.login_user(username, password)
            
            if 'error' not in api_response:
                # Registered successfully, redirect to login page
                user_login = authenticate(
                    request, username=username, password=password
                )

                # If user is authenticated, log them in
                if user_login is not None:
                    auth_login(request, user_login)                

                # Store JWT token in session
                request.session['jwt_token'] = api_response['access']

                # Redirect to a success page or render a success template
                return render(request, 'auth/login_success.html', {
                    'token': api_response['access']
                })
            else:
                form.add_error(None, api_response.get('error', 'Erro ao registrar usuário.'))
    else:
        form = LoginForm()


    return render(request, 'auth/login.html', {'form': form})