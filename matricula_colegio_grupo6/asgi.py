import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matricula_colegio_grupo6.settings')

application = get_asgi_application()
