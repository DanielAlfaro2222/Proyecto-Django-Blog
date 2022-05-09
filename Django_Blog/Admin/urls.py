from django.urls import path
from . import views

app_name = 'Admin'

urlpatterns = [
    path('', views.AdminTemplateView.as_view(), name='admin'),
    path('users/', views.UsersListView.as_view(), name='users'),
    path('users/new/', views.UserCreateView.as_view(), name='new-user'),
    path('users/edit/<slug:slug>', views.UserUpdateView.as_view(), name='edit-user'),
    path('articles/', views.ArticlesListView.as_view(), name='articles'),
    path('cities/', views.CitiesListView.as_view(), name='cities'),
    path('cities/new/', views.CityCreateView.as_view(), name='new-city'),
    path('cities/edit/<int:pk>', views.CityUpdateView.as_view(), name='edit-city'),
    path('categories/', views.CategoriesListView.as_view(), name='categories'),
    path('categories/new/', views.CategoriesCreateView.as_view(),
         name='new-category'),
    path('categories/edit/<slug:slug>',
         views.CategoryUpdateView.as_view(), name='edit-category'),
    path('articles/new/', views.ArticleCreateView.as_view(), name='new-article'),
    path('articles/edit/<slug:slug>',
         views.ArticleUpdateView.as_view(), name='edit-article'),
]
