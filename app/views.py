from typing import Any
from django import http
from django.conf import settings
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from .models import Clientes, Tour, ServiciosExtra
from . import models, forms
from .forms import ClientesForm, TourForm, ServiciosExtraForm
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView,UpdateView,DeleteView ,View
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
#@permission_required('app.add_departamento')

#Idiomas
def cambiar_idioma(request, idioma):
    if idioma in dict(settings.LANGUAGES):
        request.session['django_language'] = idioma
    return redirect(request.META.get('HTTP_REFERER', '/'))


#Usuarios
class Login(FormView):
    template_name = 'registration/login.html'
    form_class = forms.FormularioLogin
    success_url = reverse_lazy('home')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,**kwargs)
    
    def form_valid(self, form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)
    
def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

class ListadoUsuarios(ListView):
    model = models.Usuario
    template_name = 'registration/listar_usuario.html'

    def get_queryset(self):
        return self.model.objects.filter(usuario_activo = True,usuario_administrativo=True)
    
class RegistrarUsuario(CreateView):
    model = models.Usuario
    form_class = forms.FormularioUsuario
    template_name = 'registration/crear_usuario.html'
    success_url = reverse_lazy('home')

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nuevo_usuario = models.Usuario(
                email = form.cleaned_data.get('email'),
                username = form.cleaned_data.get('username'),
                nombre = form.cleaned_data.get('nombre'),
                apellidos = form.cleaned_data.get('apellidos'),
            )
            nuevo_usuario.set_password(form.cleaned_data.get('password1'))
            nuevo_usuario.save()
            login(self.request, nuevo_usuario)
            return redirect('home')
        else: 
            return render(request,self.template_name,{'form':form})

class RegistrarAdmin(CreateView):
    model = models.UsuarioManager
    form_class = forms.FormularioUsuario
    template_name = 'registration/crear_admin.html'
    success_url = reverse_lazy('login')

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nuevo_usuario = models.Usuario(
                email = form.cleaned_data.get('email'),
                username = form.cleaned_data.get('username'),
                nombre = form.cleaned_data.get('nombre'),
                apellidos = form.cleaned_data.get('apellidos'),
                usuario_administrativo = True 
            )
            nuevo_usuario.set_password(form.cleaned_data.get('password1'))
            nuevo_usuario.save()
            login(self.request, nuevo_usuario)
            return redirect('home')
        else: 
            return render(request,self.template_name,{'form':form})


# def estado_usuario(request, id):
#     usuario = get_object_or_404(models.Usuario, id=id)
#     if usuario.usuario_activo:
#         usuario.usuario_activo = False
#         messages.success(request, "Usuario eliminado")
#     else:
#         usuario.usuario_activo = True
#         messages.success(request, "Departamento activado")
#     usuario.usuario_activo.save()
#     return redirect(to='listar_cliente')

# def estado_admin(request, id):
#     usuario = get_object_or_404(models.UsuarioManager, id=id)
#     if usuario.usuario_activo:
#         usuario.usuario_activo = False
#         messages.success(request, "Usuario eliminado")
#     else:
#         usuario.usuario_activo = True
#         messages.success(request, "Usuario activado")
#     usuario.usuario_activo.save()
#     return redirect(to='listar_usuario') 

#Listar departamentos para reservar
def home(request):
    print(request.GET)
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

def administrar(request):
    return render(request, 'app/administrar.html') 

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
def detalle_departamento(request, id):
    departamento = get_object_or_404(models.Departamento, id_dep=id)

    if departamento.estado_dep == True:
        data = {
            'departamento': departamento
        }
        return render(request, 'app/Departamento/detalle_departamento.html', data)
    else: 
        return redirect('home')

    
class LoginMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')
    
class RegistrarReserva(LoginMixin,CreateView):
    model = models.Reserva
    success_url = reverse_lazy('home')

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print(request.POST)
            departamento = models.Departamento.objects.filter(id_dep =request.POST.get('departamento')).first()
            usuario = models.Usuario.objects.filter(id=request.POST.get('usuario')).first()
            if departamento and usuario:
                avance = departamento.valordiario_dep
                nueva_reserva = self.model(
                    departamento = departamento,
                    usuario = usuario,
                    avance = avance
                )
                nueva_reserva.save()
                mensaje = f'{self.model.__name__} registrada correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error,'url':self.success_url})
                response.status_code = 201
                return response

        return redirect('home')

@login_required
def ListarReservas(request):
    reservas = models.Reserva.objects.filter(usuario=request.user, estado=True)
    page = request.GET.get('page', 1)
    
    try:
        paginator = Paginator(reservas, 5)
        reservas = paginator.page(page)
    except: 
        raise Http404
    
    data = {
        'entity': reservas,
        'paginator': paginator
    }
    return render(request, 'app/listar_reservas.html', data)


class Checkin(View):
    def get(self, request, id_reserva):
        reserva = get_object_or_404(models.Reserva, id_reserva=id_reserva)
        form = forms.ReservaForm(instance=reserva)

        for field_name in form.fields:
            form.fields[field_name].disabled = True

        data = {
            'form': form
        }
        return render(request, 'app/checkin.html', data)


def cancelar_reserva(request, id_reserva):
    reserva = get_object_or_404(models.Reserva, id_reserva=id_reserva)
    
    if request.method == 'POST':
        departamento = reserva.departamento
        departamento.estado_dep = True
        departamento.save()
        reserva.save()
        
        return redirect('home')
    
    data = {
        'reserva': reserva
    }
    return render(request, 'app/cancelar_reserva.html', data)

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


#Usuarios BORRAR
# def registro(request):
#     data = {
#         'form': forms.CustomUserCreationForm()
#     }

#     if request.method == 'POST':
#         formulario = forms.CustomUserCreationForm(data=request.POST)
#         if formulario.is_valid():
#             formulario.save()
#             user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
#             login(request, user)
#             messages.success(request, "Te has registrado correctamente")
#             return redirect(to="home")
            
#     return render(request, 'registration/registro.html', data)

#/////////////////////////////////////////////////////////////////////////////////////////////////

def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'app/Tour/tour_list.html', {'tours': tours})

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, 'app/Tour/tour_detail.html',  {'tour': tour})

def tour_new(request):
    data={
        'form': TourForm()
    }
    if request.method == "POST":
        form = TourForm(data=request.POST)
        if form.is_valid():
            tour = form.save()
            return redirect('tour_detail', pk=tour.pk)
    else:
        form = TourForm()
    return render(request, 'app/Tour/tour_new.html', data)

def tour_edit(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == "POST":
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():
            tour = form.save()
            return redirect(to="tour_list")
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