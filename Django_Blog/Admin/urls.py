from django.urls import path
from . import views

app_name = 'Admin'

urlpatterns = [
    path('', views.AdminTemplateView.as_view(), name='admin'),
    path('users/', views.UsersListView.as_view(), name='users'),
    path('articles/', views.ArticlesListView.as_view(), name='articles'),
    path('cities/', views.CitiesListView.as_view(), name='cities'),
    path('categories/', views.CategoriesListView.as_view(), name='categories'),
    path('articles/new/', views.ArticleCreateView.as_view(), name='new-article'),
    path('articles/edit/<slug:slug>',
         views.ArticleUpdateView.as_view(), name='edit-article'),
]
