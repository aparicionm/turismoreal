from django.db import models 


# Create your models here.
# Modelos de tablas
class Departamento(models.Model):
    id_dep = models.AutoField(primary_key=True)
    nombre_dep = models.CharField(max_length=50, unique=True)
    direccion_dep = models.CharField(max_length=50)
    descripcion_dep = models.TextField()
    valordiario_dep = models.DecimalField(max_digits=8, decimal_places=2)
    #Inventario pk 
    #Mantención pk 
    inventario_dep = models.TextField()
    estado_dep = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to="departamentos", null=True)
    def __str__(self):
        return self.nombre_dep
    
class ImagenDepartamento(models.Model):
    imagen = models.ImageField(upload_to="departamentos")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="imagenes")


class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    fecha_comienzo = models.DateField()
    fecha_final = models.DateField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    advance = models.DecimalField(max_digits=8, decimal_places=2)
    #models.DecimalField(max_digits=8, decimal_places=0)
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


#Formulario de contacto
opciones_consultas = [
    [0, "Consulta"],
    [1, "Reclamo"],
    [2, "Sugerencia"]
]

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consultas)
    mensaje = models.TextField()
    avisos = models.BooleanField()

    def __str__(self):
        return self.nombre