from django import forms
from .models import Alumno,Apoderado,Grado,DocumentacionAdicional

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'genero', 'dni_alumno', 'fecha_nacimiento', 'colegio_procedencia', 'es_nuevo']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class ApoderadoForm(forms.ModelForm):
    class Meta:
        model = Apoderado
        fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'genero', 'dni_apoderado', 'parentesco', 'celular', 'email', 'profesion']

class DocumentacionAdicionalForm(forms.ModelForm):
    class Meta:
        model = DocumentacionAdicional
        fields = ['certificado_estudios']

class GradoForm(forms.ModelForm):
    class Meta:
        model = Grado
        fields = ['nivel', 'numero']
        
        widgets = {
            'nivel': forms.Select(), 
            'numero': forms.Select()  
        }
