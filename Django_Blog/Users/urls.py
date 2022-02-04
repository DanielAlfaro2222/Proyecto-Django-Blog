from Users import views
from django.urls import path

app_name = 'Users'

urlpatterns = [
    path('login/', views.login_view, name = 'login'),
    path('register/', views.register_view, name = 'register'),
    path('contact/', views.contact_view, name = 'contact'),
]