import re
import requests
import datetime

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from contenido.models import PaginaTube, Video
from acciones import subir_video


class Command(BaseCommand):

	'''
		TEST / SANDBOX
		Minear 20 primeras paginas de Faapy
	'''

	def handle(self, *args, **options):

		# BASE
		url_inicial = 'http://www.faapy.com'
		pagina_tube = PaginaTube.objects.get(nombre = 'faapy.com')

		''' Loop this '''

		for i in range(0, 5):

			# Links videos por page
			videos_pagina = {}

			# Generar peticion y sopa
			if i == 0:
				peticion = requests.get( url_inicial )
			else:
				peticion = requests.get( url_inicial + '/latest-updates/%s/' % str(i+1) )
			soup = BeautifulSoup( peticion.content, 'html.parser' )

			# Cojemos las urls de videos y thumbs
			for elemento_video in soup.find_all('div', { 'class' : 'thumb'}):

				url_video =  elemento_video.find('a').get('href')

				# Miramos si video existe
				try:
					Video.objects.get( url_video = url_video )
					continue
				except Video.DoesNotExist:
					pass

				thumbnail =  elemento_video.find('img').get('src')
				videos_pagina[url_video] = thumbnail


			# Recorremos pagina a pagina cada video
			for url_video, thumbnail in videos_pagina.iteritems():

				# Peticion y sopa
				peticion = requests.get( url_video )
				soup = BeautifulSoup( peticion.content, 'html.parser' )

				# Definimos variables
				titulo = soup.h1.string 
				casting = [ m.string for m in soup.find_all('a',{'class':'model-link'}) ]

				for script_tag in soup.find_all('script'):
					try:
						regex_exp = re.search('http://faapy\.com/embed/\d{1,10}',
						script_tag.string)
						codigo_iframe = regex_exp.group()
					except:
						pass

				try:
					pagina_pago = [ soup.find(attrs={"rel":"nofollow"}).string ]
				except AttributeError:
					pagina_pago = []
					
				publicado = datetime.datetime.now()

				for elemento in soup.find_all('div',{'class':'row'}):
					try:
						if 'Tags' in elemento.getText():
							tags = [ t.string for t in elemento.find_all('a') ]
					except TypeError:
						pass

				# descargamos el thumbnail
				thumb = None
				peticion_img = requests.get(thumbnail, stream=True)

				if peticion_img.status_code == 200:
					u = url_video.replace('http://faapy.com/videos/','').replace('/','_')
					path_imagen = 'static/imagenes/faapy/%s.jpg' % u
					with open( path_imagen , 'wb') as f:
						for chunk in peticion_img:
							f.write(chunk)
					thumb = path_imagen


				# Guardamos el objeto
				subir_video(
					casting,
					pagina_pago,
					pagina_tube,
					tags,
					titulo,
					thumb,
					publicado,
					url_video,
					codigo_iframe
				)




