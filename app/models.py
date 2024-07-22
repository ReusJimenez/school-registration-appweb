from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    documento_identidad = models.CharField(max_length=20, unique=True)
    es_nuevo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class DocumentacionAdicional(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    documento = models.FileField(upload_to='documentacion/')
    fecha_subida = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Documentación de {self.alumno.nombre} {self.alumno.apellido}"

class Notas(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia = models.CharField(max_length=100)
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.alumno.nombre} - {self.materia}: {self.nota}"
