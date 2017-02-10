import re
import requests
import datetime

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from contenido.models import PaginaTube, Video
from acciones import subir_video, trim


class Command(BaseCommand):

	'''
		TEST / SANDBOX
		Minear 30 primeras paginas de Eporner
	'''

	def handle(self, *args, **options):


		# numero_videos = int(args[0]) if args else 999

		#Inicio
		url_inicial = 'http://www.eporner.com/category/hd1080p/'
		pagina_tube = PaginaTube.objects.get( nombre='eporner.com' )

		for i in range(0, 3):

			# Peticion y sopa
			if i == 0:
				peticion = requests.get( url_inicial )
			else:
				peticion = requests.get( url_inicial + '%s/' % str(i))
			sopa = BeautifulSoup( peticion.content, 'html.parser' )

			# Sacamos urls a videos
			videos_pagina = []

			for video in sopa.find_all('div',{'class':'mbhd'}):

				# comprovamos si el video existe
				url_video = 'http://www.eporner.com' + video.find('a').get('href')
				try:
					video = Video.objects.get( url_video = url_video )
					continue
				except Video.DoesNotExist:
					pass

				videos_pagina.append( url_video )


			# Sacamos datos del video 
			for url_video in videos_pagina:

				# Peticion y sopa
				peticion = requests.get( url_video )
				soup = BeautifulSoup( peticion.content, 'html.parser' )

				titulo =  soup.find('h1').getText()
				publicado = datetime.datetime.now()

				# Info de la tabla ( cast y tags )
				cast = []
				tags = []
				tabla = soup.find('td',{'id':'hd-porn-tags'})
				for tr in tabla.find_all('tr'):
					
					# CAST
					if tr.strong.string == 'Pornstars:':
						for link in tr.find_all('a'):
							if 'pornstar' in link.get('href'):
								cast.append( link.string )
					# TAGS
					if tr.strong.string == 'Tags:':
						tags = [ t.string for t in tr.find_all('a') ]

				# cod iframe
				codigo_iframe = soup.find('div',{'class':'textare1'})
				codigo_iframe = BeautifulSoup(codigo_iframe.textarea.string, 'html.parser')
				codigo_iframe = codigo_iframe.iframe.get('src')

				# thumbnail
				url_thumbnail = soup.find_all('div',{'class':'cutscenesbox'})[5]
				url_thumbnail = url_thumbnail.a.get('href')

				# Descargamos el thumbnail
				request_img = requests.get(url_thumbnail, stream = True )
				thumbnail = None

				if request_img.status_code == 200:
					url_imagen = 'static/imagenes/eporner/%s.jpg' % trim(titulo)
					with open( url_imagen , 'wb') as f:
						for chunk in request_img:
							f.write(chunk)
					thumbnail = url_imagen

				# Sacamos previews
				previews = []

				for n in range(0,12):
					url_prev = soup.find_all('div',{'class':'cutscenesbox'})[n]
					url_prev = url_prev.a.get('href')

					prev_n = requests.get( url_prev, stream = True )
					if prev_n.status_code == 200:
						url_prev_n = 'static/imagenes/eporner/%s-thumb-%s.jpg' % ( trim(titulo), str(n) )
						with open( url_prev_n, 'wb') as f:
							for chunk in prev_n:
								f.write(chunk)
						previews.append(url_prev_n)

				# Guardamos el objeto
				subir_video(
					previews,
					cast,
					[],
					pagina_tube,
					tags,
					titulo,
					thumbnail,
					publicado,
					url_video,
					codigo_iframe,
				)
			# 	break
			# break


		


