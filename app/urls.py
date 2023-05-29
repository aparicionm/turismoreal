from django.urls import path
from . import views
from .views import home, contacto, agregar_Clientes, listar_Clientes, modificar_Clientes, eliminar_Clientes

urlpatterns = [
    path('', views.home, name="home"),
    path('contacto/', views.contacto, name="contacto"),
    path('agregar-Clientes/', agregar_Clientes, name="agregar_Clientes"),
    path('listar-Clientes/', listar_Clientes, name="listar_Clientes"),
    path('modificar-Clientes/<id>/', modificar_Clientes, name="modificar_Clientes"),
    path('eliminar-Clientes/<id>/', eliminar_Clientes, name="eliminar_Clientes"),
    path('agregar-departamento/', views.agregar_departamento, name="agregar_departamento"),
    path('listar-departamento/', views.listar_departamento, name="listar_departamento"),
    path('modificar-departamento/<id>/', views.modificar_departamento, name="modificar_departamento"),
    path('estado-departamento/<id>/', views.estado_departamento, name="estado_departamento"),
    path('registro/', views.registro, name="registro"),
    #path('listado-departamento', views.listado_departamento, name='listado_departamentos'),
    path('detalle-departamento/<id>/', views.detalle_departamento, name='detalle_departamento'),
    path('agregarReserva/', views.agregar_reserva,name='agregarReserva'),
    path('tours/', views.tour_list, name='tour_list'),
    path('tour/<pk>/', views.tour_detail, name='tour_detail'),
    path('tour-new/', views.tour_new, name='tour_new'),
    path('tour/<pk>/edit/', views.tour_edit, name='tour_edit'),
    path('servicios_extra/', views.servicios_extra_list, name='servicios_extra_list'),
    path('servicios_extra/<int:pk>/', views.servicios_extra_detail, name='servicios_extra_detail'),
    path('servicios_extra/create/', views.servicios_extra_create, name='servicios_extra_create'),
    path('servicios_extra/<int:pk>/update/', views.servicios_extra_update, name='servicios_extra_update'),
    path('servicios_extra/<int:pk>/delete/', views.servicios_extra_delete, name='servicios_extra_delete'),
]