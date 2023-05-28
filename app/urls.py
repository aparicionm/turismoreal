from django.urls import path
from . import views
from.views import home, contacto, galeria, agregar_Clientes, listar_Clientes, modificar_Clientes, eliminar_Clientes

urlpatterns = [
    path('', views.home, name="home"),
    path('contacto/', views.contacto, name="contacto"),
    path('galeria/', views.galeria, name="galeria"),
    path('agregar-Clientes/', agregar_Clientes, name="agregar_Clientes"),
    path('listar-Clientes/', listar_Clientes, name="listar_Clientes"),
    path('modificar-Clientes/<id>/', modificar_Clientes, name="modificar_Clientes"),
    path('eliminar-Clientes/ <id>/', eliminar_Clientes, name="eliminar_Clientes"),

]