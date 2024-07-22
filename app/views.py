from django.shortcuts import render, redirect
from .models import Alumno, DocumentacionAdicional
from .forms import AlumnoForm, DocumentacionAdicionalForm
VACANTES_TOPE = 1000

def solicitud_matricula(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save()
            if alumno.es_nuevo:
                return redirect('documentacion_adicional', alumno_id=alumno.id)
            else:
                return redirect('confirmar_matricula', alumno_id=alumno.id)
    else:
        form = AlumnoForm()
    return render(request, 'solicitud_matricula.html', {'form': form})

def verificar_vacantes(request):
    alumnos_actuales = Alumno.objects.count()
    vacantes_disponibles = VACANTES_TOPE - alumnos_actuales
    
    if vacantes_disponibles > 0:
        return render(request, 'verificar_vacantes.html', {'vacantes_disponibles': vacantes_disponibles})
    else:
        return render(request, 'solicitud_matricula.html', {'mensaje_error': 'No hay vacantes disponibles.'})

def ingresar_datos_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('confirmar_matricula')
    else:
        form = AlumnoForm()
    return render(request, 'ingresar_datos_alumno.html', {'form': form})

def documentacion_adicional(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    if request.method == 'POST':
        form = DocumentacionAdicionalForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.alumno = alumno
            doc.save()
            return redirect('confirmar_matricula', alumno_id=alumno.id)
    else:
        form = DocumentacionAdicionalForm()
    return render(request, 'documentacion_adicional.html', {'form': form})

def validar_documentacion(request):
    return render(request, 'validar_documentacion.html')

def confirmar_matricula(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    return render(request, 'confirmar_matricula.html', {'alumno': alumno})

def mostrar_constancia(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    return render(request, 'mostrar_constancia.html', {'alumno': alumno})
