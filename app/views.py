from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from .models import Alumno, Apoderado, DocumentacionAdicional, Nivel, Grado
from .forms import AlumnoForm, ApoderadoForm, DocumentacionAdicionalForm, ElegirGradoForm

# Vista Home
def home(request):
    return render(request, 'home.html')

def elegir_grado(request):
    if request.method == 'POST':
        nivel_id = request.POST.get('nivel')
        grado_id = request.POST.get('grado')

        if nivel_id and grado_id:
            try:
                grado = Grado.objects.get(id=grado_id)
                if grado.vacantes > 0:
                    # Redirigir a la página de registro de ingresantes si hay vacantes
                    return redirect('registro_ingresantes')
                else:
                    # Devolver un mensaje de error si el grado no tiene vacantes
                    messages.error(request, 'No hay vacantes disponibles para el grado seleccionado.')
            except Grado.DoesNotExist:
                messages.error(request, 'El grado seleccionado no existe.')

    niveles = Nivel.objects.all()
    return render(request, 'elegir_grado.html', {'niveles': niveles})

def get_grados(request, nivel_id):
    grados = Grado.objects.filter(nivel_id=nivel_id).values('id', 'numero', 'nivel__nivel')
    return JsonResponse(list(grados), safe=False)

# Vista Registro Ingresantes
def registro_ingresantes(request):
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST)
        apoderado_form = ApoderadoForm(request.POST)
        documentacion_form = DocumentacionAdicionalForm(request.POST, request.FILES)

        if alumno_form.is_valid() and apoderado_form.is_valid():
            alumno = alumno_form.save()
            apoderado = apoderado_form.save()
            
            # Verifica si el alumno es nuevo y maneja la documentación
            if alumno.es_nuevo:
                if documentacion_form.is_valid():
                    documentacion = documentacion_form.save(commit=False)
                    documentacion.alumno = alumno
                    documentacion.save()
                else:
                    # Manejar errores en el formulario de documentación
                    messages.error(request, 'Por favor, sube el certificado de estudios.')

            # Redirigir o mostrar un mensaje de éxito
            messages.success(request, 'Solicitud de matrícula registrada con éxito.')
            return redirect('success')  # Redirige a una página de éxito o similar

    else:
        alumno_form = AlumnoForm()
        apoderado_form = ApoderadoForm()
        documentacion_form = DocumentacionAdicionalForm()

    return render(request, 'registro_ingresantes.html', {
        'alumno_form': alumno_form,
        'apoderado_form': apoderado_form,
        'documentacion_form': documentacion_form,
    })

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