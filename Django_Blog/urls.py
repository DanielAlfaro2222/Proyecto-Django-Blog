from django.contrib import admin
from django.urls import path
from Django_Blog import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.contrib.auth import views as auth_views
from django.conf.urls import handler400
from django.conf.urls import handler403
from django.conf.urls import handler404
from django.conf.urls import handler500

urlpatterns = [
    path('', views.index_view, name='index'),
    path('users/', include('Users.urls')),
    path('blog/', include('Blog.urls')),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='recuperar-contraseña/formulario-recuperar-contraseña.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='recuperar-contraseña/recuperacion-contraseña-completado.html'),
         name='password_reset_complete'),
    path('admin/', include('Admin.urls')),
]

# Configuracion para servir la media del aplicativo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# Capturar errores del servidor para mostrar mensajes personalizados
handler400 = views.Error400TemplateView.as_view()
handler403 = views.Error403TemplateView.as_view()
handler404 = views.Error404TemplateView.as_view()
handler500 = views.Error500TemplateView.as_error_view()
