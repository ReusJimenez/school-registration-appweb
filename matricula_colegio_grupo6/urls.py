from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('verificar_vacante_grado/', views.verificar_vacante_grado, name='verificar_vacante_grado'),
    path('get_grados/<int:nivel_id>/', views.get_grados, name='get_grados'),
    #path('verificar_alumno_nuevo/', views.verificar_alumno_nuevo, name='verificar_alumno_nuevo'),
    path('registro_ingresantes/', views.registro_ingresantes, name='registro_ingresantes'),
    path('ingresar_certificado_estudios/', views.ingresar_certificado_estudios, name='ingresar_certificado_estudios'),
    path('success/', views.SuccessView.as_view(), name='success'),
]