from django.urls import path
from apps.frontend.views import article, auth, home


app_name = 'frontend'

urlpatterns = [
    path('', home.index, name='index'),
    path('register/', auth.register, name='register'),
    path('logout/', auth.logout, name='logout'),
    path('login/', auth.login, name='login'),
    path('article/', article.article_list, name='article_list'),
    path('article/<int:pk>/', article.article_detail, name='article_detail'),
    path('article/<int:pk>/comment/', article.comment_create, name='comment_create'),
]
    