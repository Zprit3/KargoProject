from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .forms import PreinscripcionForm
from reservas.models import Reserva
from .models import PerfilCliente
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.db import IntegrityError

def preinscripcion(request):
    if request.method == 'POST':
        form = PreinscripcionForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            telefono = form.cleaned_data['telefono']
            edad = form.cleaned_data['edad']
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']

            try:
                password = get_random_string(length=12)
                user = User.objects.create_user(username=email, email=email, password=password, first_name=nombre)
                Group.objects.get(name='Cliente').user_set.add(user)
                perfil = PerfilCliente.objects.create(user=user, telefono=telefono, edad=edad)
                Reserva.objects.create(cliente=perfil, fecha=fecha, hora=hora)

                messages.success(request, 'Preinscripción realizada con éxito. Se ha enviado un correo con tus datos de acceso.')
                return redirect('home')
            except IntegrityError as e:
                if 'UNIQUE constraint failed: auth_user.username' in str(e):
                    messages.error(request, 'Ya existe un usuario con este correo electrónico.')
                return render(request, 'usuarios/preinscripcion.html', {'form': form})
    else:
        form = PreinscripcionForm()
    return render(request, 'usuarios/preinscripcion.html', {'form': form})