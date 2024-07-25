from django.db import models

class Apoderado(models.Model):
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    genero = models.CharField(max_length=10, blank=True, null=True)  
    dni_apoderado = models.CharField(max_length=20, unique=True)
    parentesco = models.CharField(max_length=50, blank=True, null=True) 
    celular = models.CharField(max_length=9, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profesion = models.CharField(max_length=100, blank=True, null=True)

    def _str_(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno} ({self.dni_apoderado})"

class Alumno(models.Model):
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    genero = models.CharField(max_length=10, blank=True, null=True)  
    dni_alumno = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    colegio_procedencia = models.CharField(max_length=100, blank=True, null=True)
    es_nuevo = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno} ({self.dni_alumno})"

class DocumentacionAdicional(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    certificado_estudios = models.FileField(upload_to='documentacion/')
    fecha_subida = models.DateField(auto_now_add=True)

class Nivel(models.Model):
    nivel = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nivel

class Grado(models.Model):
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, related_name='grados')
    numero = models.PositiveSmallIntegerField()
    vacantes = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.numero} - {self.nivel.nivel}"
