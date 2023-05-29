from django.shortcuts import render, redirect, get_object_or_404
from .models import Clientes
from . import models, forms
from .forms import ClientesForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
#@permission_required('app.add_departamento')
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
            data["mensaje"] = "Contacto enviado"
        else:
            data["form"] = formulario
    return render(request, 'app/contacto.html', data)

def galeria (request):
    return render(request, 'app/galeria.html')

#Departamento
def agregar_departamento(request):
    data = {
        'form':forms.DepartamentoForm()
    }

    if request.method == 'POST':
        formulario = forms.DepartamentoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Departamento agregado")
        else: 
            data["form"] = formulario
    return render(request, 'app/Departamento/agregar.html', data)

def listar_departamento(request):
    departamentos = models.Departamento.objects.all()
    page = request.GET.get('page', 1)
    
    try:
        paginator = Paginator(departamentos, 5)
        departamentos = paginator.page(page)
    except: 
        raise Http404
    
    data = {
        'entity': departamentos,
        'paginator': paginator
    }
    return render(request, 'app/Departamento/listar.html', data)

def modificar_departamento(request, id):
    departamento = get_object_or_404(models.Departamento, id_dep=id)
    data = {
        'form': forms.DepartamentoForm(instance=departamento)
    }
    if request.method == 'POST':
        formulario = forms.DepartamentoForm(data=request.POST, instance=departamento, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Departamento modificado correctamente")
            return redirect(to='listar_departamento') 
        data["form"] = formulario
    return render(request, 'app/Departamento/modificar.html', data)

def estado_departamento(request, id):
    departamento = get_object_or_404(models.Departamento, id_dep=id)
    if departamento.estado_dep:
        departamento.estado_dep = False
        messages.success(request, "Departamento desactivado")
    else:
        departamento.estado_dep = True
        messages.success(request, "Departamento activado")
    departamento.save()
    return redirect(to='listar_departamento') 

#Cliente
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


#Usuarios
def registro(request):
    data = {
        'form': forms.CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = forms.CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="home")
            
    return render(request, 'registration/registro.html', data)

