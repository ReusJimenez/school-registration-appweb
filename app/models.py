from django.db import models

class Apoderado(models.Model):
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    #genero (masculino, femenino)
    dni_apoderado = models.CharField(max_length=20, unique=True)
    #parentesco con alumno
    #celular
    #email
    #profesion
    
    #def __str__(self):

class Alumno(models.Model):
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    #genero (masculino, femenino)
    dni_alumno = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    #colegio de procedencia
    es_nuevo = models.BooleanField(default=True)
    #solo verifica dni_alumno, avisa si algun dato esta incorrecto o si no es alumno antiguo
    
    #def __str__(self):

class DocumentacionAdicional(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    certificado_estudios = models.FileField(upload_to='documentacion/')
    fecha_subida = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Documentación de {self.alumno.nombre} {self.alumno.apellido}"

#para sacar vacantes y avisar
class Nivel(models.Model):
    #Nivel

class Grado(models.Model):
    #Grado
