from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *

GENDER_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro'),
)

class CustomRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Ingresa un nombre de usuario ",
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        max_length=150,
        help_text='',
        required=True
    )
    password1 = forms.CharField(
        label="Ingresa una contraseña ",
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        help_text='',
        required=True
    )
    password2 = forms.CharField(
        label="Confirma tu contraseña ",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña'}),
        help_text='',
        required=True
    )
    email = forms.EmailField(
    label="Ingresa tu Correo Electrónico  ",
    widget=forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}),
    required=True
)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UserEditForm(UserCreationForm):

    email = forms.EmailField(label="Ingrese su email:")
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirma la contraseña', widget=forms.PasswordInput)

    last_name = forms.CharField(label="Apellido ")
    first_name = forms.CharField(label="Nombre ")

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'last_name', 'first_name']
        
class cambiarAvatar(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['imagen']
        
class HeladoForm(forms.ModelForm):
    class Meta:
        model = Helado
        fields = ['nombre', 'imagen', 'descripcion_corta', 'descripcion_larga']

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')

        if not imagen and not self.instance.imagen:
            raise forms.ValidationError('Este campo es obligatorio. Por favor, sube una imagen.')

        return imagen
        
class PastelForm(forms.ModelForm):
    class Meta:
        model = Pastel
        fields = '__all__'
        
class BatidoForm(forms.ModelForm):
    class Meta:
        model = Batido
        fields = '__all__'

class InfantilForm(forms.ModelForm):
    class Meta:
        model = Infantil
        fields = '__all__'