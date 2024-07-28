from django import forms
from .models import Alumno, Apoderado, DocumentacionAdicional, Nivel, Grado

class ApoderadoForm(forms.ModelForm):
    genero = forms.ChoiceField(
        choices=[('', 'Seleccione'), ('M', 'Masculino'), ('F', 'Femenino')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Género'
    )

    class Meta:
        model = Apoderado
        fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'genero', 'dni_apoderado', 'parentesco', 'celular', 'email', 'profesion']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control required-field', 'placeholder': 'Ingrese sus nombres'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control required-field', 'placeholder': 'Ingrese su apellido paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control required-field', 'placeholder': 'Ingrese su apellido materno'}),
            'dni_apoderado': forms.TextInput(attrs={'class': 'form-control required-field', 'placeholder': 'Ingrese el DNI del apoderado'}),
            'parentesco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el parentesco'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de celular'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el email'}),
            'profesion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la profesión'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.error_messages = {
                    'required': f'Complete {field.label}'
                }

class AlumnoForm(forms.ModelForm):
    genero = forms.ChoiceField(
        choices=[('', 'Seleccione'), ('M', 'Masculino'), ('F', 'Femenino')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Género'
    )

    class Meta:
        model = Alumno
        fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'genero', 'dni_alumno', 'fecha_nacimiento', 'colegio_procedencia', 'es_nuevo']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control required-field', 'placeholder': 'Ingrese sus nombres'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control required-field', 'placeholder': 'Ingrese su apellido paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control required-field', 'placeholder': 'Ingrese su apellido materno'}),
            'dni_alumno': forms.TextInput(attrs={'class': 'form-control required-field', 'placeholder': 'Ingrese el DNI del apoderado'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'colegio_procedencia': forms.TextInput(attrs={'class': 'form-control required-field', 'placeholder': 'Ingrese el colegio de procedencia'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.error_messages = {
                    'required': f'Complete {field.label}'
                }

class DocumentacionAdicionalForm(forms.ModelForm):
    class Meta:
        model = DocumentacionAdicional
        fields = ['certificado_estudios']
        widgets = {
            'certificado_estudios': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.error_messages = {
                    'required': f'Complete {field.label}'
                }

class ElegirGradoForm(forms.Form):
    nivel = forms.ModelChoiceField(queryset=Nivel.objects.all(), required=True)
    grado = forms.ModelChoiceField(queryset=Grado.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        nivel_id = kwargs.pop('nivel_id', None)
        super().__init__(*args, **kwargs)
        if nivel_id:
            self.fields['grado'].queryset = Grado.objects.filter(nivel_id=nivel_id)
