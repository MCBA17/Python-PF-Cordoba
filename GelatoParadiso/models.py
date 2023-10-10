from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Avatar(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    imagen = models.ImageField(upload_to='avatares', null=True, blank = True)
 
    def __str__(self):
        return f"{self.user} - {self.imagen}"
    
class Helado(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion_corta = models.TextField(default="Descripción por defecto corta")
    descripcion_larga = models.TextField(default="Descripción por defecto")
    imagen = models.ImageField(upload_to='helados/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class Pastel(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion_corta = models.TextField(default="Descripción por defecto corta")
    descripcion_larga = models.TextField(default="Descripción por defecto")
    imagen = models.ImageField(upload_to='pasteles/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
class Batido(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion_corta = models.TextField(default="Descripción por defecto corta")
    descripcion_larga = models.TextField(default="Descripción por defecto")
    imagen = models.ImageField(upload_to='batidos/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class Infantil(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion_corta = models.TextField(default="Descripción por defecto corta")
    descripcion_larga = models.TextField(default="Descripción por defecto")
    imagen = models.ImageField(upload_to='infantil/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre