"""
URL configuration for matricula_colegio_grupo6 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('iniciar_matricula/', views.iniciar_matricula, name='iniciar_matricula'),
    path('verificar_vacantes/', views.verificar_vacantes, name='verificar_vacantes'),
    path('ingresar_datos_alumno/', views.ingresar_datos_alumno, name='ingresar_datos_alumno'),
    path('documentacion_adicional/<int:alumno_id>/', views.documentacion_adicional, name='documentacion_adicional'),
    path('validar_documentacion/<int:alumno_id>/', views.validar_documentacion, name='validar_documentacion'),
    path('verificar_notas/<int:alumno_id>/', views.verificar_notas, name='verificar_notas'),
    path('confirmar_matricula/<int:alumno_id>/', views.confirmar_matricula, name='confirmar_matricula'),
    path('registrar_matricula/<int:alumno_id>/', views.registrar_matricula, name='registrar_matricula'),
    path('enviar_constancia/<int:alumno_id>/', views.enviar_constancia, name='enviar_constancia'),
]