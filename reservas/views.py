from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from .forms import ReservaForm, UsuarioForm
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from usuarios.models import PerfilCliente
from django.contrib import messages
from django.db import IntegrityError, models, connection
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Reserva, Pista
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def crear_reserva(request):
    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST)
        reserva_form = ReservaForm(request.POST)
        if usuario_form.is_valid() and reserva_form.is_valid():
            user = usuario_form.save()
            try:
                cliente_group = Group.objects.get(name="Cliente")
                user.groups.add(cliente_group)
            except Group.DoesNotExist:
                messages.error(
                    request,
                    "Error: El grupo 'Cliente' no existe. Contacte al administrador.",
                )
                user.delete()
                return render(
                    request,
                    "reservas/crear_reserva.html",
                    {"usuario_form": usuario_form, "reserva_form": reserva_form},
                )
            perfil = PerfilCliente.objects.create(
                user=user,
                telefono=reserva_form.cleaned_data["telefono"],
                edad=reserva_form.cleaned_data["edad"],
            )
            reserva = reserva_form.save(commit=False)
            reserva.cliente = perfil
            try:
                reserva.save()
                messages.success(request, "Reserva creada exitosamente.")
                base_url = reverse("pagina_de_exito")
                query_params = urlencode({"fecha": reserva.fecha, "hora": reserva.hora})
                url = f"{base_url}?{query_params}"
                return HttpResponseRedirect(url)
            except IntegrityError:
                messages.error(
                    request,
                    "Ya existe una reserva para esa pista, fecha y hora. Por favor, elige otra opción.",
                )
                user.delete()
                perfil.delete()
                return render(
                    request,
                    "reservas/crear_reserva.html",
                    {"usuario_form": usuario_form, "reserva_form": reserva_form},
                )
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")

    else:
        usuario_form = UsuarioForm()
        reserva_form = ReservaForm()

    return render(
        request,
        "reservas/crear_reserva.html",
        {"usuario_form": usuario_form, "reserva_form": reserva_form},
    )


def pagina_de_exito(request):
    fecha = request.GET.get("fecha")
    hora = request.GET.get("hora")
    context = {"fecha": fecha, "hora": hora}
    return render(request, "reservas/exito.html", context)


class ListaReservasAdmin(ListView):
    model = Reserva
    template_name = "reservas/lista_reservas_admin.html"
    context_object_name = "reservas"
    ordering = ["fecha", "hora"]  # Ordena las reservas por fecha y hora por defecto

    def get_queryset(self):
        # Obtiene todas las reservas
        return Reserva.objects.all()

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required
def lista_mis_reservas(request):
    try:
        perfil = request.user.perfil
        reservas = Reserva.objects.filter(cliente=perfil).order_by("fecha", "hora")
        return render(
            request, "reservas/lista_mis_reservas.html", {"reservas": reservas}
        )
    except PerfilCliente.DoesNotExist:
        messages.error(
            request,
            "No tienes un perfil de cliente asociado. Contacta al administrador.",
        )
        return redirect("home")


@method_decorator(user_passes_test(lambda u: u.is_staff), name="dispatch")
class PistaCreateView(CreateView):
    model = Pista
    fields = "__all__"  # Incluye todos los campos del modelo en el formulario
    template_name = "reservas/pista_form.html"
    success_url = reverse_lazy("lista_pistas")

    def form_valid(self, form):
        messages.success(self.request, "Pista creada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrige los errores en el formulario.")
        return super().form_invalid(form)


@method_decorator(user_passes_test(lambda u: u.is_staff), name="dispatch")
class PistaUpdateView(UpdateView):
    model = Pista
    fields = "__all__"
    template_name = "reservas/pista_form.html"
    success_url = reverse_lazy("lista_pistas")

    def form_valid(self, form):
        messages.success(self.request, "Pista actualizada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrige los errores en el formulario.")
        return super().form_invalid(form)


@method_decorator(user_passes_test(lambda u: u.is_staff), name="dispatch")
class PistaDeleteView(DeleteView):
    model = Pista
    template_name = "reservas/pista_confirm_delete.html"
    success_url = reverse_lazy("lista_pistas")
    context_object_name = "pista"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Pista eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)


@method_decorator(user_passes_test(lambda u: u.is_staff), name="dispatch")
class ListaPistas(ListView):
    model = Pista
    template_name = "reservas/lista_pistas.html"
    context_object_name = "pistas"


@login_required
@user_passes_test(lambda u: u.is_staff)  # Solo usuarios staff (admin)
def asignar_pista(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    pistas_disponibles = []

    if request.method == "POST":
        pista_id = request.POST.get("pista")
        if pista_id:
            pista = get_object_or_404(Pista, id=pista_id)
            # Esto verifica la disponibilidad
            reservas_en_mismo_horario = Reserva.objects.filter(
                pista=pista, fecha=reserva.fecha, hora=reserva.hora
            ).count()
            if reservas_en_mismo_horario < pista.capacidad_por_turno:
                reserva.pista = pista
                reserva.save()
                messages.success(
                    request, f"Pista {pista.nombre} asignada a la reserva."
                )
                return redirect("lista_reservas_admin")
            else:
                messages.error(
                    request,
                    f"La pista {pista.nombre} no tiene capacidad disponible para esa fecha y hora.",
                )
        else:
            messages.error(request, "Debes seleccionar una pista.")

    # Obtener pistas disponibles para la fecha y hora de la reserva
    # Obtener las pistas que no tienen reservas en ese horario o que tienen menos reservas que su capacidad
    pistas_disponibles = Pista.objects.annotate(
        num_reservas=Count(
            "reservas",
            filter=models.Q(reservas__fecha=reserva.fecha, reservas__hora=reserva.hora),
        )
    ).filter(
        models.Q(num_reservas__lt=models.F("capacidad_por_turno"))
        | models.Q(num_reservas__isnull=True)
    )

    return render(
        request,
        "reservas/asignar_pista.html",
        {"reserva": reserva, "pistas": pistas_disponibles},
    )


class ReservaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reserva
    fields = ['fecha', 'hora']
    template_name = 'reservas/reserva_form.html'
    context_object_name = 'reserva' # Para acceder a la reserva en el template

    def get_object(self, queryset=None):
        reserva_id = self.kwargs.get('pk')
        return get_object_or_404(Reserva, pk=reserva_id)

    def test_func(self):
        reserva = self.get_object()
        return reserva.cliente.user == self.request.user

    def get_success_url(self):
        messages.success(self.request, "Reserva modificada exitosamente.")
        return reverse('lista_mis_reservas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reserva'] = self.object
        return context



@login_required
@user_passes_test(lambda u: u.is_staff)
def cambiar_estado_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        if nuevo_estado in [choice[0] for choice in Reserva.ESTADO_CHOICES]:
            reserva.estado = nuevo_estado
            reserva.save()
            messages.success(
                request,
                f"Estado de la reserva cambiado a {reserva.get_estado_display()}.",
            )
        else:
            messages.error(request, "Estado no válido.")

    return redirect("lista_reservas_admin")

@user_passes_test(lambda u: u.is_staff)
def eliminar_cliente(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        if reserva.cliente and reserva.cliente.user:
            usuario = reserva.cliente.user
            usuario.delete()
            messages.success(request, "Cliente eliminado exitosamente.")
        else:
            messages.error(request, "No se pudo eliminar el cliente.")
        return redirect('lista_reservas_admin')
    return render(request, 'reservas/confirmar_eliminar_cliente.html', {'reserva': reserva})


@login_required
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    reserva_table = Reserva._meta.db_table 
    pista_table = Pista._meta.db_table
    with connection.cursor() as cursor:
        try:
            cursor.execute(f"""  # Usa f-string para formatear la consulta
                SELECT
                    p.nombre AS nombre_pista,
                    r.estado,
                    COUNT(r.cliente_id) AS cantidad_clientes
                FROM
                    {reserva_table} r  -- Usa el nombre real de la tabla
                JOIN
                    {pista_table} p ON r.pista_id = p.id
                WHERE
                    r.fecha = CURRENT_DATE
                    AND r.hora BETWEEN CURRENT_TIME - INTERVAL '1 hour' AND CURRENT_TIME + INTERVAL '1 hour'
                GROUP BY
                    p.nombre, r.estado
                ORDER BY
                    p.nombre, r.estado;
            """)
            resultados = cursor.fetchall()
        except Exception as e:
            print(f"Error en la consulta SQL: {e}")
            return render(request, 'reservas/dashboard.html', {'error': str(e)})

    context = {'resultados': resultados}
    return render(request, 'reservas/dashboard.html', context)