from django import forms
from .models import  Clientes
from . import models



class ClientesForm(forms.ModelForm):

    class Meta:
        model = Clientes 
        fields = '__all__'

#Formulario de contacto
class ContactoForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))   
    correo = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    tipo_consulta = forms.CharField(widget=forms.Select(attrs={"class":"form-control mb-3"}, choices=[
        ("separator", "----------"),
        (0, "Consulta"),
        (1, "Reclamo"),
        (2, "Sugerencia")]))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control mb-3"}))
    avisos = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class":"form-control mb-3"}))
    class Meta:
        model = models.Contacto
        fields = '__all__'
        #fields = ["nombre", "correo", "tipo_consulta", "mensaje", "aviso"]

