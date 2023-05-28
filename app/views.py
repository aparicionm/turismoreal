from django.shortcuts import render, redirect, get_object_or_404
from .models import Clientes
from . import models, forms
from .forms import ClientesForm


# Create your views here.
def home (request):
    departamentos = models.Departamento.objects.all()
    data = {
        'departamentos': departamentos
    }
    return render(request, 'app/home.html', data)

def contacto (request):
    data = {
        'form': forms.ContactoForm()
    }
    if request.method == 'POST':
        formulario = forms.ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "contacto enviado"
        else:
            data["form"] = formulario
    return render(request, 'app/contacto.html', data)

def galeria (request):
    return render(request, 'app/galeria.html')


def agregar_Clientes(request):
    
    data = {

        'form': ClientesForm()

    }

    if request.method == 'POST':
        formulario=ClientesForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Guardado Correctamente"
        else:
            data["form"] = formulario

    return render(request,'app/Clientes/agregar.html',data)


def listar_Clientes(request):

    cliente = Clientes.objects.all()
     
    data = {

        'cliente': cliente
    }

    return render(request,'app/Clientes/listar.html', data)


def modificar_Clientes(request, id):

    cliente = get_object_or_404(Clientes, id=id )

    data = {

        'form': ClientesForm(instance=cliente)

    }

    if request.method == 'POST':
        formulario = ClientesForm(data=request.POST, instance=cliente) 
        if formulario.is_valid():
             formulario.save()  
             return  redirect(to="listar_Clientes")
        data["form"] = formulario
    return render(request, 'app/Clientes/modificar.html', data)





def eliminar_Clientes(request, id): 
        cliente = get_object_or_404(Clientes, id=id)
        cliente.delete()
        return redirect(to="listar_Clientes")

