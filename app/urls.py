from django.urls import path
from . import views
from .views import home, contacto, galeria, agregar_Clientes, listar_Clientes, modificar_Clientes, eliminar_Clientes

urlpatterns = [
    path('', views.home, name="home"),
    path('contacto/', views.contacto, name="contacto"),
    path('galeria/', views.galeria, name="galeria"),
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
    #path('detalle-departamento/<id>/', views.DetalleDepartamento, name='detalle_departamento')

]