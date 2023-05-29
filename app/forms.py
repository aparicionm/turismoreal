from django import forms
from .models import  Clientes
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError


class ClientesForm(forms.ModelForm):
    nombre_cliente = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    rut_cliente = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    email_cliente = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))

    class Meta:
        model = Clientes 
        fields = '__all__'

#Usuario (usar para crear usuarios clientes y también, no usar login.css)
#class UserForm(forms.ModelForm):
#    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
#    password = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    
#Formulario de contacto

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

class ContactoForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))   
    correo = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    tipo_consulta = forms.CharField(widget=forms.Select(attrs={"class":"form-select mb-3"}, choices=[
        ("separator", "----------"),
        (0, "Consulta"),
        (1, "Reclamo"),
        (2, "Sugerencia")]))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control mb-3"}))
    avisos = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class":"form-check mb-3"}))

    class Meta:
        model = models.Contacto
        fields = '__all__'
        #fields = ["nombre", "correo", "tipo_consulta", "mensaje", "aviso"]

#Formularios de Departamento
class DepartamentoForm(forms.ModelForm):
    nombre_dep = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))   
    direccion_dep = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    descripcion_dep = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control mb-3"}))
    valordiario_dep = forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    inventario_dep = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control mb-3"}))
    #estado_dep = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class":"form-check mb-3"}))
    #imagen

    '''
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre_dep"]
        existe = models.departamento.objects.filter(nombre_dep__iexact=nombre).exists()
        if existe:
            raise ValidationError("Este nombre ya existe")
        return nombre
    '''

    class Meta:
        model = models.Departamento
        exclude = ['estado_dep'] 
        #fields = ["nombre_dep","direccion_dep","descripcion_dep","valordiario_dep","inventario_dep","imagen"]

