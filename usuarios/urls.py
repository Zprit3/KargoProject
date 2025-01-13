from django.urls import path
from . import views

urlpatterns = [
    path('preinscripcion/', views.preinscripcion, name='preinscripcion'),
]