from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Modelo para los servicios de consultoría de Akkü
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

# Modelo para las estrategias de datos y growth
class Estrategia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

# Modelo para el formulario de contacto (Prospectos)
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()

# Modelo para tus posts de LinkedIn y Portfolio
class Post(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=150)
    cuerpo = RichTextField()
    imagen = models.ImageField(upload_to='blog_images', null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    autor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.titulo} | {self.autor}"

# --- SISTEMA DE CHAT / MENSAJERÍA ---
class Mensaje(models.Model):
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enviados')
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recibidos')
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.emisor.username} para {self.receptor.username}"
    
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatares', null=True, blank=True)
    biografia = models.TextField(null=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - Perfil"
    
    