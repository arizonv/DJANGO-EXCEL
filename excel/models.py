from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
