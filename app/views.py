from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import Alumno, Apoderado, DocumentacionAdicional, Nivel, Grado
from .forms import AlumnoForm, ApoderadoForm, DocumentacionAdicionalForm, ElegirGradoForm

# Vista Home
def home(request):
    return render(request, 'home.html')

# Vista Elegir Grado
def elegir_grado(request):
    if request.method == 'POST':
        form = ElegirGradoForm(request.POST)
        if form.is_valid():
            grado = form.cleaned_data['grado']
            if grado.vacantes > 0:
                return redirect('registro_ingresantes', grado_id=grado.id)
            else:
                messages.error(request, 'No hay vacantes disponibles para el grado seleccionado.')
    else:
        form = ElegirGradoForm()
    
    return render(request, 'elegir_grado.html', {'form': form})

# Vista Registro Ingresantes
def registro_ingresantes(request, grado_id):
    grado = Grado.objects.get(id=grado_id)
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST)
        apoderado_form = ApoderadoForm(request.POST)
        
        if alumno_form.is_valid() and apoderado_form.is_valid():
            apoderado = apoderado_form.save()
            alumno = alumno_form.save(commit=False)
            alumno.grado = grado
            alumno.save()
            
            if alumno.es_nuevo:
                return redirect('ingresar_certificado_estudios', alumno_id=alumno.id)
            else:
                messages.success(request, 'Alumno registrado exitosamente.')
                return redirect('home')
    else:
        alumno_form = AlumnoForm()
        apoderado_form = ApoderadoForm()

    return render(request, 'registro_ingresantes.html', {'alumno_form': alumno_form, 'apoderado_form': apoderado_form, 'grado': grado})

# Vista Ingresar Certificado de Estudios
def ingresar_certificado_estudios(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    if request.method == 'POST':
        form = DocumentacionAdicionalForm(request.POST, request.FILES)
        if form.is_valid():
            documentacion = form.save(commit=False)
            documentacion.alumno = alumno
            documentacion.save()
            messages.success(request, 'Felicidades, se registró con éxito.')
            return redirect('home')
    else:
        form = DocumentacionAdicionalForm()
    
    return render(request, 'ingresar_certificado_estudios.html', {'form': form})