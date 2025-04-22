from django.contrib.messages import get_messages
from django.conf import settings
from django.shortcuts import redirect, render
from apps.frontend.forms import RegisterForm
from apps.frontend.services.api_auth import register_user
from django.contrib.auth import authenticate, login, logout as auth_logout

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
            api_response = register_user(user)

            if 'error' not in api_response:
                # Registered successfully, redirect to login page
                user_login = authenticate(
                    request, username=user.username, password=form.cleaned_data['password']
                )

                # If user is authenticated, log them in
                if user_login is not None:
                    login(request, user_login)                

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