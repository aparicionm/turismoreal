from django.db import models 
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.signals import post_save,pre_save

# Create your models here.
# Modelos de tablas

class UsuarioManager(BaseUserManager):
    def create_user(self,email,username,nombre,apellidos,password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        
        usuario = self.model(
            username = username,
            email = self.normalize_email(email),
            nombre = nombre,
            apellidos = apellidos
        )

        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_superuser(self,username,email,nombre,apellidos,password):
        usuario = self.create_user(
            email,
            username = username,
            nombre = nombre,
            apellidos = apellidos,
            password = password
        )
        usuario.usuario_administrativo = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de usuario', unique=True,max_length=100)
    email = models.EmailField('Correo electrónico', max_length=254,unique=True)
    rut = models.CharField('Rut', max_length=10, blank=True, null=False)
    nombre = models.CharField('Nombre', max_length=200, blank=True, null=True)
    apellidos = models.CharField('Apellidos', max_length=200, blank=True, null=True)
    imagen = models.ImageField('Foto de perfil', upload_to='perfil/', height_field=None, width_field=None, max_length=200, blank=True, null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrativo = models.BooleanField(default=False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellidos']

    def __str__(self):
        return f'{self.nombre},{self.apellidos}'
    
    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrativo

class Departamento(models.Model):
    id_dep = models.AutoField(primary_key=True)
    nombre_dep = models.CharField('Nombre departamento', max_length=50, unique=True)
    ciudad_dep = models.CharField('Ciudad', max_length=50, null=True)
    direccion_dep = models.CharField('Dirección', max_length=50)
    descripcion_dep = models.TextField('Descripción', )
    valordiario_dep = models.DecimalField('Valor diario', max_digits=8, decimal_places=2)
    #Inventario pk 
    #Mantención pk 
    inventario_dep = models.TextField('Inventario')
    estado_dep = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to="departamentos", null=True)
    def __str__(self):
        return self.nombre_dep
    
class ImagenDepartamento(models.Model):
    imagen = models.ImageField(upload_to="departamentos")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="imagenes")

    
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

    def __str__(self):
        return self.nombre



class Tour(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class ServiciosExtra(models.Model):
    nombre = models.CharField(max_length=100)
    wifi = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
    


class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True)
    servicio_extra = models.ForeignKey(ServiciosExtra, on_delete=models.CASCADE,null=True)
    cant_dias = models.SmallIntegerField('Cantidad de dias a reservar', default=1)
    avance = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_creacion = models.DateField('Fecha de creacion', auto_now = True, auto_now_add= False)
    estado = models.BooleanField(default= True, verbose_name='Estado')
    #models.DecimalField(max_digits=8, decimal_places=0)
    #id_dep = models.ForeignKey(Departamento, related_name='reserva_id_dep', to_field='id_dep', on_delete=models.PROTECT)
    #nombre_dep = models.ForeignKey(Departamento, related_name='reserva_nombre_dep', to_field='nombre_dep', on_delete=models.PROTECT)
    #id_tour
    #id_servicio extra

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'Reserva de Departamento {self.departamento} por {self.usuario}'
    
def reservado(sender,instance,**kwargs):
    departamento = instance.departamento
    if departamento.estado_dep == True:
        departamento.estado_dep = False
        departamento.save()

post_save.connect(reservado,sender=Reserva)