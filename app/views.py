from django.shortcuts import render, redirect, get_object_or_404
from .models import Clientes, Tour, ServiciosExtra
from . import models, forms
from .forms import ClientesForm, TourForm, ServiciosExtraForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required



# Create your views here.
#@permission_required('app.add_departamento')

#Listar departamentos para reservar
def home(request):
    departamentos = models.Departamento.objects.filter(estado_dep=True)
    page = request.GET.get('page', 1)
    
    try:
        paginator = Paginator(departamentos, 100)
        departamentos = paginator.page(page)
    except: 
        raise Http404
    
    data = {
        'entity': departamentos,
        'paginator': paginator
    }
    return render(request, 'app/home.html', data)
#fabi bug
'''
def home (request):
    departamentos = models.Departamento.objects.all()
    data = {
        'departamentos': departamentos
    }
    return render(request, 'app/home.html', data)
'''
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

#Reservar departamentos

'''
def ListadoDepartamentos(request):
    model = models.Departamento
    template_name = 'app/Departamento/listado_departamentos.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(estado_departamento = True)
        return render(request, queryset)


def DetalleDepartamento(request):
    model = models.Departamento
    template = 'app/Departamento/detalle_departamento.html'

    def get_objects(self):
        try:
            instance = self.model.objects.get(id_dep = self.kwargs['id'])
        except expression as identifier:
            pass

        return instance
    
    def get_context_data(self, **kwargs):
        context = {}
        context['object'] = self.get_object()
        return context
    
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,self.get_context_data())
'''

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

#/////////////////////////////////////////////////////////////////////////////////////////////////

def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'app/Tour/tour_list.html', {'tours': tours})

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, 'app/Tour/tour_detail.html',  {'tour': tour})

def tour_new(request):
    if request.method == "POST":
        form = TourForm(request.POST)
        if form.is_valid():
            tour = form.save()
            return redirect('tour_detail', pk=tour.pk)
    else:
        form = TourForm()
    return render(request, 'app/Tour/tour_edit.html', {'form': form})

def tour_edit(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == "POST":
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():
            tour = form.save()
            return redirect('tour_detail', pk=tour.pk)
    else:
        form = TourForm(instance=tour)
    return render(request, 'app/Tour/tour_edit.html', {'form': form})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def servicios_extra_list(request):
    servicios_extra = ServiciosExtra.objects.all()
    return render(request, 'app/ServiciosExtra/servicios_extra_list.html', {'servicios_extra': servicios_extra})

def servicios_extra_detail(request, pk):
    servicio_extra = get_object_or_404(ServiciosExtra, pk=pk)
    return render(request, 'app/ServiciosExtra/servicios_extra_detail.html', {'servicio_extra': servicio_extra})

def servicios_extra_create(request):
    if request.method == 'POST':
        form = ServiciosExtraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicios_extra_list')
    else:
        form = ServiciosExtraForm()
    return render(request, 'app/ServiciosExtra/servicios_extra_form.html', {'form': form})

def servicios_extra_update(request, pk):
    servicio_extra = get_object_or_404(ServiciosExtra, pk=pk)
    if request.method == 'POST':
        form = ServiciosExtraForm(request.POST, instance=servicio_extra)
        if form.is_valid():
            form.save()
            return redirect('servicios_extra_list')
    else:
        form = ServiciosExtraForm(instance=servicio_extra)
    return render(request, 'app/ServiciosExtra/servicios_extra_form.html', {'form': form})

def servicios_extra_delete(request, pk):
    servicio_extra = get_object_or_404(ServiciosExtra, pk=pk)
    servicio_extra.delete()
    return redirect('servicios_extra_list')