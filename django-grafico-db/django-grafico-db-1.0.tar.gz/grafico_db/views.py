from django.shortcuts import render
from django.core.management import call_command
# Create your views here.

import os
def mostrar_grafico(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	dir = os.path.join(os.path.dirname(BASE_DIR), "site-packages")
	
	ruta = dir+"/grafico_db/static/grafico_db/imagen.png"
	print ruta
	call_command('graph_models','--all-applications', '--group-models', '--output', ruta)

	return render(request, 'index.html')