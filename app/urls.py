from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .views import home, contacto, agregar_Clientes, listar_Clientes, modificar_Clientes, eliminar_Clientes

urlpatterns = [
    path('', views.home, name="home"),
    path('contacto/', views.contacto, name="contacto"),
    path('administrar/', staff_member_required(views.administrar), name="administrar"),
    #USUARIOS
    path('listado_usuarios/', staff_member_required(views.ListadoUsuarios.as_view()), name= 'listar_usuario'),
    path('registrar_usuario/', views.RegistrarUsuario.as_view(), name= 'registrar_usuario'),
    path('registrar_admin/', staff_member_required(views.RegistrarAdmin.as_view()), name= 'registrar_admin'),
    #CLIENTES
    path('agregar-Clientes/', staff_member_required(agregar_Clientes), name="agregar_Clientes"),
    path('listar-Clientes/', staff_member_required(listar_Clientes), name="listar_Clientes"),
    path('modificar-Clientes/<id>/', staff_member_required(modificar_Clientes), name="modificar_Clientes"),
    path('eliminar-Clientes/<id>/', staff_member_required(eliminar_Clientes), name="eliminar_Clientes"),
    #DEPARTAMENTOS
    path('agregar-departamento/', staff_member_required(views.agregar_departamento), name="agregar_departamento"),
    path('listar-departamento/', staff_member_required(views.listar_departamento), name="listar_departamento"),
    path('modificar-departamento/<id>/', staff_member_required(views.modificar_departamento), name="modificar_departamento"),
    path('estado-departamento/<id>/', staff_member_required(views.estado_departamento), name="estado_departamento"),
    #Reservas
    path('listar-reservas/', views.ListarReservas, name="listar_reservas"),
    path('checkin/<int:id_reserva>/', views.Checkin.as_view(), name="checkin"),
    path('reservas/cancelar/<int:id_reserva>/', views.cancelar_reserva, name='cancelar_reserva'),
    #path('registro/', views.registro, name="registro"),
    #path('listado-departamento', views.listado_departamento, name='listado_departamentos'),
    path('detalle-departamento/<id>/', views.detalle_departamento, name='detalle_departamento'),
    path('reservar-departamento/', views.RegistrarReserva.as_view(),name='reservar_departamento'),
    #TOURS
    path('tours/', staff_member_required(views.tour_list), name='tour_list'),
    path('tour/<pk>/', staff_member_required(views.tour_detail), name='tour_detail'),
    path('tour-new/', staff_member_required(views.tour_new), name='tour_new'),
    path('tour/<pk>/edit/', staff_member_required(views.tour_edit), name='tour_edit'),
    #SERVICIOS
    path('servicios_extra/', staff_member_required(views.servicios_extra_list), name='servicios_extra_list'),
    path('servicios_extra/<int:pk>/', staff_member_required(views.servicios_extra_detail), name='servicios_extra_detail'),
    path('servicios_extra/create/', staff_member_required(views.servicios_extra_create), name='servicios_extra_create'),
    path('servicios_extra/<int:pk>/update/', staff_member_required(views.servicios_extra_update), name='servicios_extra_update'),
    path('servicios_extra/<int:pk>/delete/', staff_member_required(views.servicios_extra_delete), name='servicios_extra_delete'),
]