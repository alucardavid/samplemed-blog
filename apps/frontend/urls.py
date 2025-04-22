from django.urls import path
from apps.frontend.views import auth, home


app_name = 'frontend'

urlpatterns = [
    path('', home.index, name='index'),
    path('register/', auth.register, name='register'),
]
    