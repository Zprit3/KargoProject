from django.contrib import admin, messages
from django.contrib.auth.models import User
from .models import PerfilCliente

def eliminar_clientes(modeladmin, request, queryset):
    for perfil in queryset:
        if perfil.user:
            usuario = perfil.user
            usuario.delete()
    messages.success(request, f"{queryset.count()} clientes eliminados.")
eliminar_clientes.short_description = "Eliminar clientes seleccionados"

@admin.register(PerfilCliente)
class PerfilClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'edad')
    search_fields = ('user__username', 'telefono')
    actions = [eliminar_clientes]