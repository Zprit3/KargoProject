from django.contrib import admin
from django.urls import path, include
from kargo import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservas.urls')),
    path('', include('usuarios.urls')),
    path('', views.home, name='home'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('galeria/', views.galeria, name='galeria'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]