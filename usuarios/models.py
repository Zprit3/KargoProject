from django.db import models
from django.contrib.auth.models import User

class PerfilCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil') # Relación 1 a 1
    telefono = models.CharField(max_length=20, blank=True)
    edad = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username