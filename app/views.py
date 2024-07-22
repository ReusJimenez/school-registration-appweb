from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Estudiante, Vacante, Nota
from .forms import EstudianteForm, EstudianteExistenteForm

def inicio(request):
    return render(request, 'inicio.html')

def matricula(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        grado = request.POST.get('grado')

        # Verificar si el estudiante ya está registrado
        estudiante = Estudiante.objects.filter(nombre=nombre, apellido=apellido, grado=grado).first()

        if estudiante:
            # Estudiante existente
            return redirect('confirmar_datos', estudiante_id=estudiante.id)
        else:
            # Estudiante nuevo
            form = EstudianteForm(request.POST, request.FILES)
            if form.is_valid():
                # Verificar vacantes
                vacante = Vacante.objects.filter(grado=form.cleaned_data['grado']).first()
                if vacante and vacante.vacantes_disponibles > 0:
                    form.save()
                    vacante.vacantes_disponibles -= 1
                    vacante.save()
                    return HttpResponse("Matrícula confirmada")
                else:
                    return HttpResponse("No hay vacantes disponibles")
    else:
        form = EstudianteForm()
    return render(request, 'matricula.html', {'form': form})

def confirmar_datos(request, estudiante_id):
    estudiante = Estudiante.objects.get(id=estudiante_id)
    if request.method == 'POST':
        # Verificar vacantes
        vacante = Vacante.objects.filter(grado=estudiante.grado).first()
        if vacante and vacante.vacantes_disponibles > 0:
            vacante.vacantes_disponibles -= 1
            vacante.save()
            return HttpResponse("Matrícula confirmada")
        else:
            return HttpResponse("No hay vacantes disponibles")

    return render(request, 'confirmar_datos.html', {'estudiante': estudiante})
