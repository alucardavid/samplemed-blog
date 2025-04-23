from django.urls import path
from apps.frontend.views import article, auth, home


app_name = 'frontend'

urlpatterns = [
    path('', home.index, name='index'),
    path('register/', auth.register, name='register'),
    path('logout/', auth.logout, name='logout'),
    path('login/', auth.login, name='login'),
    path('article/', article.article_list, name='article_list'),
]
    