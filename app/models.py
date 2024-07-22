from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    documento_identidad = models.CharField(max_length=20)
    es_nuevo = models.BooleanField(default=False)

class DocumentacionAdicional(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    documento = models.FileField(upload_to='documentacion/')
    fecha_subida = models.DateField(auto_now_add=True)

class Vacante(models.Model):
    disponible = models.BooleanField(default=True)

class Matricula(models.Model):
    alumno = models.OneToOneField(Alumno, on_delete=models.CASCADE)
