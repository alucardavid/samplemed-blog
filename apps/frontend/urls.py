from django.urls import path
from apps.frontend.views import home


app_name = 'frontend'

urlpatterns = [
    path('', home.index, name='index'),
]
    