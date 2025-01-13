from django import forms
from .models import Reserva
from django.forms import DateInput, TimeInput
from django.contrib.auth.forms import UserCreationForm

class ReservaForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100, label="Nombre")
    email = forms.EmailField(label="Correo Electrónico")
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono")
    edad = forms.IntegerField(required=False, label="Edad")

    class Meta:
        model = Reserva
        fields = ['fecha', 'hora']
        widgets = {
            'fecha': DateInput(attrs={'type': 'date'}),
            'hora': TimeInput(attrs={'type': 'time'}),
        }

class UsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("first_name",) 
        labels = { 
            'first_name': 'Nombre',
        }