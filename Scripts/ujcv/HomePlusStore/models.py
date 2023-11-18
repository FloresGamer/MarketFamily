from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class Rol(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    contraseña = models.CharField(max_length=255)
    correo_electronico = models.EmailField(unique=True)
    numero_telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    SEXO_CHOICES = (
        ('M', 'M'),
        ('F', 'F'),
    )
    sexo = models.CharField(max_length=20, choices=SEXO_CHOICES)
    
    direccion = models.TextField()
    foto_de_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)

@receiver(post_save, sender=Usuario)
def set_rol_cliente_signal(sender, instance, created, **kwargs):
    if created and not instance.rol:
        # Assuming 1 is the ID of the "cliente" role, change it accordingly
        cliente_role = Rol.objects.get(pk=1)
        instance.rol = cliente_role
        instance.save()
    
def get_masked_password(self):
    return '*' * len(self.contraseña)

class CategoriaArticulo(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class PrecioHistorico(models.Model):
    articulo = models.ForeignKey('Articulo', on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.articulo.nombre} - {self.precio} - {self.fecha}"

class Articulo(models.Model):
    id_articulo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_ultima_modificacion = models.DateTimeField(auto_now=True)
    imagen = models.ImageField(upload_to='imagenes_articulos/', null=True, blank=True)  
    categoria = models.ForeignKey(CategoriaArticulo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre
    

class Cargo(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    sueldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.nombre
    
class Departamento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    

class Documentopersonal(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Colaborador(models.Model):
    id_colaborador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    Documentopersonal = models.ForeignKey(Documentopersonal, on_delete=models.CASCADE, default=1)
    documento_identidad = models.FileField(upload_to='documentos/', null=True, blank=True)  
    direccion = models.TextField()
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    fecha_nacimiento = models.DateField()
    correo_electronico = models.EmailField()
    numero_telefono = models.CharField(max_length=20)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    fecha_contratacion = models.DateField(auto_now_add=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, default=1)  # 1 is assumed to be the ID of the "empleado" role
    perfil = models.ImageField(upload_to='perfil/', null=True, blank=True)
    contraseña = models.CharField(max_length=255, default='mi_valor_predeterminado')
 
    def sueldo_cargo(self):
        return self.cargo.sueldo  

    def __str__(self):
        return f"{self.id_colaborador}: {self.nombre} {self.apellido}"

# Señal para asignar el rol empleado cuando se crea un Colaborador
@receiver(post_save, sender=Colaborador)
def set_rol_empleado_signal(sender, instance, created, **kwargs):
    if created and not instance.rol:
        # Assuming 2 is the ID of the "empleado" role, change it accordingly
        empleado_role = Rol.objects.get(pk=2)
        instance.rol = empleado_role
        instance.save()


class Sucursal(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    direccion = models.TextField()
    fecha_inauguracion = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    

class HistoricoCargo(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    cargo_anterior = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_cambio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.colaborador.nombre} - {self.cargo_anterior.nombre} - {self.fecha_cambio}"

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    sucursal = models.ForeignKey('Sucursal', on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad_disponible = models.PositiveIntegerField()

    def __str__(self):
        return f"Inventario en {self.sucursal.nombre} - {self.articulo.nombre}: {self.cantidad_disponible}"





# Create your models here.
