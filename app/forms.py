from django import forms
from .models import Alumno, DocumentacionAdicional

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'documento_identidad', 'es_nuevo']

class DocumentacionAdicionalForm(forms.ModelForm):
    class Meta:
        model = DocumentacionAdicional
        fields = ['documento']