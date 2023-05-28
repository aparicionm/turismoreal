from django.db import models 


# Create your models here.

class Departamento(models.Model):
    id_dep = models.AutoField(primary_key=True)
    nombre_dep = models.CharField(max_length=50, unique=True)
    direcicion_dep = models.CharField(max_length=50)
    descripcion_dep = models.TextField()
    valordiario_dep = models.DecimalField(max_digits=8, decimal_places=2)
    #Inventario pk 
    #Mantención pk 
    inventario_dep = models.TextField()
    estado_dep = models.BooleanField()
    def __str__(self):
        return self.nombre_dep

class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    fecha_comienzo = models.DateField()
    fecha_final = models.DateField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    advance = models.DecimalField(max_digits=8, decimal_places=2)
    id_dep = models.ForeignKey(Departamento, related_name='reserva_id_dep', to_field='id_dep', on_delete=models.PROTECT)
    nombre_dep = models.ForeignKey(Departamento, related_name='reserva_nombre_dep', to_field='nombre_dep', on_delete=models.PROTECT)
    #id_tour
    def __str__(self):
        return self.precio
    
class Clientes(models.Model):
    #id_clientes = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=50, unique=True)
    rut_cliente = models.CharField(max_length=50, unique=True)
    email_cliente = models.CharField(max_length=50, unique=True)
    #apellido_clientes = models.CharField(max_length=50, unique=True)
    #direcicion_clientes = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_cliente

