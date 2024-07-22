from django.shortcuts import render, redirect
from .models import Alumno, DocumentacionAdicional, Vacante, Matricula
from .forms import AlumnoForm, DocumentacionAdicionalForm

def iniciar_matricula(request):
    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save()
            return redirect('verificar_vacantes')
    else:
        form = AlumnoForm()
    return render(request, 'matricula/iniciar_matricula.html', {'form': form})

def verificar_vacantes(request):
    vacantes_disponibles = Vacante.objects.filter(disponible=True).exists()
    if not vacantes_disponibles:
        return render(request, 'matricula/no_vacantes.html')
    return redirect('ingresar_datos_alumno')

def ingresar_datos_alumno(request):
    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save()
            if alumno.es_nuevo:
                return redirect('documentacion_adicional', alumno_id=alumno.id)
            else:
                return redirect('verificar_notas', alumno_id=alumno.id)
    else:
        form = AlumnoForm()
    return render(request, 'matricula/ingresar_datos_alumno.html', {'form': form})

def documentacion_adicional(request, alumno_id):
    if request.method == "POST":
        form = DocumentacionAdicionalForm(request.POST, request.FILES)
        if form.is_valid():
            documentacion = form.save(commit=False)
            documentacion.alumno_id = alumno_id
            documentacion.save()
            return redirect('validar_documentacion', alumno_id=alumno_id)
    else:
        form = DocumentacionAdicionalForm()
    return render(request, 'matricula/documentacion_adicional.html', {'form': form})

def validar_documentacion(request, alumno_id):
    documentacion = DocumentacionAdicional.objects.filter(alumno_id=alumno_id).first()
    if not documentacion:
        return render(request, 'matricula/documentacion_invalida.html')
    return redirect('confirmar_matricula', alumno_id=alumno_id)

def verificar_notas(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    return redirect('confirmar_matricula', alumno_id=alumno_id)

def confirmar_matricula(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    return render(request, 'matricula/confirmacion_matricula.html', {'alumno': alumno})

def registrar_matricula(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    matricula = Matricula(alumno=alumno)
    matricula.save()
    return redirect('enviar_constancia', alumno_id=alumno_id)

def enviar_constancia(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    return render(request, 'matricula/constancia_matricula.html', {'alumno': alumno})
