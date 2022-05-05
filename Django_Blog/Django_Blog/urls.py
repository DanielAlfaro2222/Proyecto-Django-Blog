from django.contrib import admin
from django.urls import path
from Django_Blog import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name = 'index'),
    path('users/', include('Users.urls')),
    path('blog/', include('Blog.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name ='password_reset_complete'),
]

# Configuracion para servir la media del aplicativo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)