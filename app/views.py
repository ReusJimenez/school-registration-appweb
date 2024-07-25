from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Alumno, Apoderado, DocumentacionAdicional, Grado
from .forms import AlumnoForm, ApoderadoForm, DocumentacionAdicionalForm

# Vista Home
def home(request):
    return render(request, 'app/home.html')

# Vista Elegir Grado
def elegir_grado(request):
    if request.method == 'POST':
        nivel = request.POST.get('nivel')
        grado = request.POST.get('grado')
        # Verificar vacantes
        vacantes_disponibles = Grado.objects.filter(nivel=nivel, numero=grado, vacantes__gt=0).exists()
        if not vacantes_disponibles:
            return render(request, 'app/elegir_grado.html', {'error': 'Vacantes llenas'})
        else:
            return redirect('registro_ingresantes', nivel=nivel, grado=grado)
    return render(request, 'app/elegir_grado.html')

# Vista Registro Ingresantes
def registro_ingresantes(request, nivel, grado):
    if request.method == 'POST':
        form_apoderado = ApoderadoForm(request.POST)
        form_alumno = AlumnoForm(request.POST)
        if form_apoderado.is_valid() and form_alumno.is_valid():
            apoderado = form_apoderado.save()
            alumno = form_alumno.save(commit=False)
            alumno.apoderado = apoderado
            alumno.grado = Grado.objects.get(nivel=nivel, numero=grado)
            alumno.save()
            if alumno.es_nuevo:
                return redirect('ingresar_certificado_estudios', alumno_id=alumno.id)
            else:
                return HttpResponse('Solicitud enviada correctamente')
    else:
        form_apoderado = ApoderadoForm()
        form_alumno = AlumnoForm()
    return render(request, 'app/registro_ingresantes.html', {'form_apoderado': form_apoderado, 'form_alumno': form_alumno})

# Vista Ingresar Certificado de Estudios
def ingresar_certificado_estudios(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    if request.method == 'POST':
        form = DocumentacionAdicionalForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.alumno = alumno
            doc.save()
            return HttpResponse('Solicitud enviada correctamente')
    else:
        form = DocumentacionAdicionalForm()
    return render(request, 'app/ingresar_certificado_estudios.html', {'form': form})
