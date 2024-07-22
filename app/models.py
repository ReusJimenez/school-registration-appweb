from django.db import models

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    grado = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    es_nuevo = models.BooleanField(default=True)
    # Documentación adicional para alumnos nuevos
    documento_identidad = models.CharField(max_length=50, blank=True)
    certificado_nacimiento = models.FileField(upload_to='certificados/', blank=True)
    comprobante_domicilio = models.FileField(upload_to='comprobantes/', blank=True)

class Vacante(models.Model):
    grado = models.CharField(max_length=50)
    vacantes_disponibles = models.PositiveIntegerField()

class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    asignatura = models.CharField(max_length=100)
    calificacion = models.FloatField()
    fecha = models.DateField()
