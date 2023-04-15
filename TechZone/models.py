from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    producto = models.CharField(max_length=40)
    precio = models.CharField(max_length=100)
    titulo = models.CharField(max_length=40)
    estado = models.CharField(max_length=5)
    descripcion = models.CharField(max_length=500)
    publisher = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="publisher")
    imagen = models.ImageField(upload_to="products", null=True, blank=True)
    item1 = models.CharField(max_length=100)
    item2 = models.CharField(max_length=100)
    item3 = models.CharField(max_length=100)
    creado_el = models.DateTimeField(auto_now_add=True)
    
    def image_url(self):
        return self.imagen.url if self.imagen else ''

    def __str__(self):
        return f"{self.titulo} -- {self.precio}"
    
class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="profile")
    imagen = models.ImageField(upload_to="profiles", null=True, blank=True)
    info = models.CharField(max_length=250)

class Mensaje(models.Model):
    mensaje = models.TextField(max_length=1000)
    email = models.EmailField()
    destinatario = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="destinatario")