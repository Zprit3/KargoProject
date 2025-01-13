from django.urls import path
from . import views

urlpatterns = [
    path('reservar/', views.crear_reserva, name='crear_reserva'),
    path('exito/', views.pagina_de_exito, name='pagina_de_exito'),
    path('reservas/admin/', views.ListaReservasAdmin.as_view(), name='lista_reservas_admin'), # Lista para admin
    path('mis-reservas/', views.lista_mis_reservas, name='lista_mis_reservas'), # Lista para clientes
    path('pistas/', views.ListaPistas.as_view(), name='lista_pistas'),
    path('pistas/crear/', views.PistaCreateView.as_view(), name='crear_pista'),
    path('pistas/editar/<int:pk>/', views.PistaUpdateView.as_view(), name='editar_pista'),
    path('pistas/eliminar/<int:pk>/', views.PistaDeleteView.as_view(), name='eliminar_pista'),
    path('reservas/asignar/<int:reserva_id>/', views.asignar_pista, name='asignar_pista'),
    path('mis-reservas/editar/<int:pk>/', views.ReservaUpdateView.as_view(), name='editar_reserva'),
    path('reservas/cambiar_estado/<int:reserva_id>/', views.cambiar_estado_reserva, name='cambiar_estado_reserva'),
    path('reservas/eliminar_cliente/<int:reserva_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('dashboard/', views.dashboard, name='dashboard'),
]