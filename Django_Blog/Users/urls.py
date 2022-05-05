from Users import views
from django.urls import path

app_name = 'Users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('contact/', views.contact_view, name='contact'),
    path('logout/', views.logout_view, name='logout'),
    path('author/<slug:slug>', views.AuthorDetailView.as_view(), name='author'),
    path('account/', views.AccountTemplateView.as_view(), name='account'),
    path('update-data/', views.update_data_user, name='update-data-user'),
    path('articles/', views.PublicationsListView.as_view(), name='articles-user'),
    path('new-article/', views.CreateArticleView.as_view(), name='new-article'),
    path('edit-article/<slug:slug>',
         views.UpdateArticleView.as_view(), name='edit-article')
]
