from django import forms
from .models import  Clientes, Tour, ServiciosExtra 
from . import models 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

#Usuarios
class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

class FormularioUsuario(forms.ModelForm):
    password1 = forms.CharField(label = 'Contraseña',widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control mb-3',
            'placeholder': 'Ingrese su contraseña',
            'id': 'password1',
            'required': 'required',
        }
    ))

    password2 = forms.CharField(label = 'Contraseña de confirmación',widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control mb-3',
            'placeholder': 'Ingrese nuevamente su contraseña',
            'id': 'password2',
            'required': 'required',
        }
    ))

    class Meta:
        model = models.Usuario
        fields = ('email', 'username','rut','nombre','apellidos')
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'Correo electrónico'
                }
            ),

            'rut': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'Rut'
                }
            ),


            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'Ingrese su nombre'
                }
            ),

            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'Ingrese su o sus apellidos'
                }
            ),

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'Ingrese su nombre de usuario'
                }
            ),
        }
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    
    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    

#Tablas
class ReservaForm(forms.ModelForm):
    class Meta:
        model = models.Reserva
        exclude = ['estado']
        widgets = {
            'departamento': forms.Select(attrs={'class': 'form-control mb-3'}),
            'usuario': forms.Select(attrs={'class': 'form-control mb-3'}),
            'tour': forms.Select(attrs={'class': 'form-control mb-3'}),
            'servicio_extra': forms.Select(attrs={'class': 'form-control mb-3'}),
            'cant_dias': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'avance': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
        }

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

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

class ContactoForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))   
    correo = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    tipo_consulta = forms.CharField(widget=forms.Select(attrs={"class":"form-select mb-3"}, choices=[
        ("separator", "----------"),
        (0, "Consulta"),
        (1, "Reclamo"),
        (2, "Sugerencia")]))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control mb-3"}))

    class Meta:
        model = models.Contacto
        fields = '__all__'
        #fields = ["nombre", "correo", "tipo_consulta", "mensaje", "aviso"]

#Formularios de Departamento
class DepartamentoForm(forms.ModelForm):
    nombre_dep = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))   
    ciudad_dep = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))   
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

class TourForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))  
    descripcion = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control mb-3"}))
    departamento = forms.ModelChoiceField(queryset=models.Departamento.objects.all(), widget=forms.Select(attrs={"class":"form-select mb-3"}))
    class Meta:
        model = Tour
        fields = ('nombre', 'descripcion', 'departamento')


class ServiciosExtraForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"})) 
    wifi = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class":"form-check mb-3"}))
    reseñas = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control mb-3"}))
    class Meta:
        model = ServiciosExtra
        fields = '__all__'
