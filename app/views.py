from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import Alumno, Apoderado, DocumentacionAdicional, Nivel, Grado
from .forms import AlumnoForm, ApoderadoForm, DocumentacionAdicionalForm, ElegirGradoForm

def home(request):
    return render(request, 'home.html')

def verificar_vacante_grado(request):
    if request.method == 'POST':
        nivel_id = request.POST.get('nivel')
        grado_id = request.POST.get('grado')

        if nivel_id and grado_id:
            try:
                grado = Grado.objects.get(id=grado_id)
                if grado.vacantes > 0:
                    request.session['grado_id'] = grado_id
                    return redirect('verificar_alumno_nuevo')
                else:
                    messages.error(request, 'No hay vacantes disponibles para el grado seleccionado.')
            except Grado.DoesNotExist:
                messages.error(request, 'El grado seleccionado no existe.')

    niveles = Nivel.objects.all()
    return render(request, 'verificar_vacante_grado.html', {'niveles': niveles})

def get_grados(request, nivel_id):
    grados = Grado.objects.filter(nivel_id=nivel_id).values('id', 'numero', 'nivel__nivel')
    return JsonResponse(list(grados), safe=False)

def verificar_alumno_nuevo(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        if Alumno.objects.filter(dni_alumno=dni).exists():
            alumno = Alumno.objects.get(dni_alumno=dni)
            request.session['alumno_id'] = alumno.id
            messages.success(request, 'DNI verificado. Puedes proceder al registro.')
            return redirect('registro_ingresantes')
        else:
            messages.error(request, 'El DNI no está registrado. Puedes proceder con el registro de un nuevo alumno.')
            return redirect('registro_ingresantes')

    return render(request, 'verificar_alumno_nuevo.html')

def registro_ingresantes(request):
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST)
        apoderado_form = ApoderadoForm(request.POST)
        documentacion_form = DocumentacionAdicionalForm(request.POST, request.FILES)

        if alumno_form.is_valid() and apoderado_form.is_valid() and documentacion_form.is_valid():
            alumno = alumno_form.save()
            apoderado = apoderado_form.save()
            documentacion = documentacion_form.save(commit=False)
            documentacion.alumno = alumno
            documentacion.save()

            grado_id = request.session.get('grado_id')
            if grado_id:
                grado = get_object_or_404(Grado, id=grado_id)
                if grado.vacantes > 0:
                    grado.vacantes -= 1
                    grado.save()
                else:
                    messages.error(request, 'No hay vacantes disponibles para el grado seleccionado.')
                    return redirect('verificar_vacante_grado')
            else:
                messages.error(request, 'No se pudo determinar el grado.')
                return redirect('verificar_vacante_grado')

            messages.success(request, 'Solicitud de matrícula registrada con éxito.')
            return redirect('success')

    else:
        alumno_form = AlumnoForm()
        apoderado_form = ApoderadoForm()
        documentacion_form = DocumentacionAdicionalForm()

    return render(request, 'registro_ingresantes.html', {
        'alumno_form': alumno_form,
        'apoderado_form': apoderado_form,
        'documentacion_form': documentacion_form,
    })

class SuccessView(TemplateView):
    template_name = 'success.html'
