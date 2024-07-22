from django import forms
from .models import Estudiante

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'grado', 'direccion', 'documento_identidad', 'certificado_nacimiento', 'comprobante_domicilio']

class EstudianteExistenteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'grado']
