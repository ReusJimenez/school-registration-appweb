from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import Alumno, Apoderado, DocumentacionAdicional, Nivel, Grado
from .forms import AlumnoForm, ApoderadoForm, DocumentacionAdicionalForm, ElegirGradoForm

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
                    return redirect('registro_ingresantes')
                else:
                    messages.error(request, 'No hay vacantes disponibles para el grado seleccionado.')
            except Grado.DoesNotExist:
                messages.error(request, 'El grado seleccionado no existe.')

    niveles = Nivel.objects.all()
    return render(request, 'elegir_grado.html', {'niveles': niveles})

def get_grados(request, nivel_id):
    grados = Grado.objects.filter(nivel_id=nivel_id).values('id', 'numero', 'nivel__nivel')
    return JsonResponse(list(grados), safe=False)

def registro_ingresantes(request):
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST)
        apoderado_form = ApoderadoForm(request.POST)
        documentacion_form = DocumentacionAdicionalForm(request.POST, request.FILES)

        if alumno_form.is_valid() and apoderado_form.is_valid():
            alumno = alumno_form.save()
            apoderado = apoderado_form.save()
            
            # Si el alumno es nuevo, redirige a ingresar_certificado_estudios
            if alumno.es_nuevo:
                request.session['alumno_id'] = alumno.id  # Guarda el ID del alumno en la sesión
                return redirect('ingresar_certificado_estudios')

            # Si no es nuevo, guardar y mostrar mensaje de éxito
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

def ingresar_certificado_estudios(request):
    # Verificar si el alumno_id está en la sesión
    if 'alumno_id' not in request.session:
        return redirect('elegir_grado')  # Redirige a elegir_grado si no hay alumno_id en la sesión

    # Obtener y eliminar el alumno_id de la sesión
    alumno_id = request.session.pop('alumno_id')  

    # Manejo del formulario POST
    if request.method == 'POST':
        documentacion_form = DocumentacionAdicionalForm(request.POST, request.FILES)
        
        # Verificar si el formulario es válido
        if documentacion_form.is_valid():
            alumno = Alumno.objects.get(id=alumno_id)
            documentacion = documentacion_form.save(commit=False)
            documentacion.alumno = alumno
            documentacion.save()
            
            # Mensaje de éxito y redirección
            messages.success(request, "Felicidades, se registró con éxito.")
            return redirect('success')
        else:
            messages.error(request, 'Por favor, sube el certificado de estudios.')
    else:
        documentacion_form = DocumentacionAdicionalForm()

    # Renderizar el formulario
    return render(request, 'ingresar_certificado_estudios.html', {'documentacion_form': documentacion_form})

class SuccessView(TemplateView):
    template_name = 'success.html'
