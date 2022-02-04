from django.contrib import admin
from django.urls import path
from Django_Blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name = 'index'),
]

# Configuracion para servir la media del aplicativo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)