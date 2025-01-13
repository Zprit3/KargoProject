from django.db import models
from usuarios.models import PerfilCliente


class Pista(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=(('niños', 'Niños'), ('jovenes', 'Jóvenes'), ('adultos', 'Adultos')))
    capacidad_por_turno = models.IntegerField()

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    cliente = models.ForeignKey(PerfilCliente, on_delete=models.CASCADE, related_name='reservas')
    pista = models.ForeignKey(Pista, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservas')
    fecha = models.DateField()
    hora = models.TimeField()

    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_CONFIRMADA = 'confirmada'
    ESTADO_CANCELADA = 'cancelada'
    ESTADO_FINALIZADA = 'finalizada'

    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_CONFIRMADA, 'Confirmada'),
        (ESTADO_CANCELADA, 'Cancelada'),
        (ESTADO_FINALIZADA, 'Finalizada'),
    ]

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)

    def __str__(self):
        return f"Reserva de {self.cliente.user.username} el {self.fecha} a las {self.hora}"
    
    class Meta:
        unique_together = ('pista', 'fecha', 'hora')
        ordering = ['fecha', 'hora']