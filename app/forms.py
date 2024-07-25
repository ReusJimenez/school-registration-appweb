from django import forms
from .models import Alumno,Apoderado,DocumentacionAdicional,Nivel,Grado

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

class ElegirGradoForm(forms.Form):
    nivel = forms.ModelChoiceField(queryset=Nivel.objects.all(), required=True)
    grado = forms.ModelChoiceField(queryset=Grado.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        nivel_id = kwargs.pop('nivel_id', None)
        super().__init__(*args, **kwargs)
        if nivel_id:
            self.fields['grado'].queryset = Grado.objects.filter(nivel_id=nivel_id)
