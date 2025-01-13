from django.contrib import admin, messages
from .models import Pista, Reserva
from django.contrib.auth.models import User

@admin.register(Pista)
class PistaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'capacidad_por_turno')
    list_filter = ('tipo',)
    search_fields = ('nombre',)

def cancelar_reservas(modeladmin, request, queryset):
    queryset.update(estado=Reserva.ESTADO_CANCELADA)
    messages.success(request, f"{queryset.count()} reservas canceladas.")
cancelar_reservas.short_description = "Cancelar reservas seleccionadas"

def eliminar_clientes(modeladmin, request, queryset):
    for reserva in queryset:
        if reserva.cliente and reserva.cliente.user: #verifica si existe cliente y usuario
            usuario = reserva.cliente.user
            usuario.delete()
    messages.success(request, f"{queryset.count()} clientes eliminados.")
eliminar_clientes.short_description = "Eliminar clientes de las reservas seleccionadas"


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'pista', 'fecha', 'hora', 'estado')
    list_filter = ('fecha', 'estado')
    search_fields = ('cliente__user__username', 'pista__nombre')
    date_hierarchy = 'fecha'
    actions = [cancelar_reservas, eliminar_clientes] 

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser: #si es superusuario, ve todas las reservas
            return qs
        return qs.filter(cliente__user=request.user) #si no es superusuario, que solo ve sus reservas

    fieldsets = (
        (None, {
            'fields': ('cliente', 'pista', 'fecha', 'hora', 'estado')
        }),
    )
    
