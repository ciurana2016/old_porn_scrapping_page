import re
import json
import requests
import dateutil.parser

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from contenido.models import PaginaTube, Video
from acciones import subir_video


class Command(BaseCommand):

	'''
		Comando diaria para hacer scraping de WWW.BEEG.COM
		
		Copiado literlamente de beeg_sandbox_1.py
	'''

	def handle(self, *args, **options):

		# Variables necesarias
		pagina_tube = PaginaTube.objects.get( nombre = 'beeg.com' )
		url_paginatube = 'http://www.beeg.com'
		paginas_video = []

		# Peticion y creacion de sopa
		peticion = requests.get( url_paginatube )
		soup = BeautifulSoup( peticion.content, 'html.parser' )

		# Sacamos las ids de videos del javascript de la pag
		# y las guardamos
		for script in soup.find_all('script'):
			try:
				regex = re.search('\[(\d{7},?)+\]', script.string)
				paginas_video += json.loads( regex.group() )
			except:
				continue

		# Recorremos todas las paginas para extraer la info
		for pagina in paginas_video:

			# Miramos si video existe
			try:
				Video.objects.get( url_video = url_paginatube + '/' + str(pagina) )
				continue
			except Video.DoesNotExist:
				pass

			# Peticion y sopa
			peticion = requests.get( url_paginatube + '/' + str(pagina) )
			soup = BeautifulSoup( peticion.content, 'html.parser' )

			# Definimos variables para guardar el vid
			pag_pago_1 = soup.find(title="Visit Paysite").string
			pag_pago_2 = soup.find(title="Visit Network").string
			pagina_pago = [pag_pago_1, pag_pago_2]

			titulo = soup.find('title').string[:-8]
			url_video = url_paginatube + '/' + str(pagina)

			meta_tags = soup.findAll(attrs={"name":"keywords"})[0]
			tags = meta_tags.get('content').split(',')

			# Cast y datetime estan en una tabla
			casting = []
			for elemento in soup.find_all('tr'):

				if 'Cast' in str(elemento):
					if ',' in str(elemento):
						for c in elemento.find('td').string.split(','):
							casting.append( c )
					else:
						casting.append( elemento.find('td').string )

				elif 'Published' in str(elemento):
					publicado = elemento.find('td').string
					publicado = dateutil.parser.parse( publicado )


			# Dejamos para el final descargar el thumbnail
			request_img = requests.get('http://img.beeg.com/320x240/%s.jpg' % str(pagina), stream=True)

			thumbnail = None

			if request_img.status_code == 200:
				url_imagen = 'static/imagenes/beeg/%s.jpg' % str(pagina)
				with open( url_imagen , 'wb') as f:
					for chunk in request_img:
						f.write(chunk)
				thumbnail = url_imagen



			# Ahora que tenemos todas las variables necesarias llamamos a 
			
			# def subir_video(
			# 	casting,
			# 	pagina_pago,
			# 	pagina_tube,
			# 	tags,
			# 	titulo,
			# 	thumbnail,
			# 	publicado = False,
			# 	url_video = '',
			# 	codigo_iframe = ''):
			
			subir_video(
				casting,
				pagina_pago,
				pagina_tube,
				tags,
				titulo,
				thumbnail,
				publicado,
				url_video
			)

			# break


		


