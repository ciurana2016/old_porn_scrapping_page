import re
import json
import requests
import dateutil.parser

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from contenido.models import PaginaTube, Video, Preview
from acciones import subir_video


class Command(BaseCommand):

	'''
		Comando diario para ahcer scraping de WWW.PORNTUBE.COM 
		Minear 5 primeras pagins de Porntube

		Copiado literalmente de porntube_sandbox_1.py
	'''

	def handle(self, *args, **options):

		url_paginatube = 'http://www.porntube.com'
		pagina_tube = PaginaTube.objects.get( nombre = 'porntube.com' )

		# loopeamos las 3 primeras paginas
		for pagina in range(0, 11):

			# Hacemos request y definimos sopa
			if pagina == 0:
				peticion = requests.get( url_paginatube )
			else:
				peticion = requests.get( url_paginatube +'/videos?p=%s' % str(pagina + 1))
			soup = BeautifulSoup( peticion.content, 'html.parser' )

			# Metemos todos los videos y thumbs de esa pagina
			# en un array
			videos = {}

			elementos_video = soup.find_all('div' , { 'class' : 'thumb_video' })
			for video in elementos_video:

				# Comprovamos si es hd
				hd = video.find('li', {'class':'topHD'})
				if hd == None: continue

				url_video = video.find('a').get('href')
				imagen_video = video.find('img').get('data-original')
				videos[url_video] = imagen_video


			# Recorremos todos los videos
			for video, imagen in videos.iteritems():

				# A vences ponen videos que no son de porntube
				if '4tube' in video:
					continue
				if 'pornerbros' in video:
					continue
				
				# Miramos si video existe
				if not video: continue
				try:
					Video.objects.get( url_video = video )
					continue
				except Video.DoesNotExist:
					pass

				# Peticion y sopa
				
				# Ajustar la url, nueva version va directo a link /video
				# Sin poner delante el http...
				video = 'http://www.porntube.com%s' % video
				peticion = requests.get(video)
				soup = BeautifulSoup( peticion.content, 'html.parser' )

				# Cojemos variables
				iframe = soup.find('textarea', { 'id' : 'textarea-iframe' }).string
				iframe = BeautifulSoup(iframe, 'html.parser')
				codigo_iframe = iframe.find('iframe').get('src')
				pagina_pago =[soup.find('a', {'class':'item-to-subscribe'}).string]
				titulo = str(soup.title)[7:][:-22]
				url_video = video

				casting = []
				try:
					actores = soup.find( 'ul', {'class':'pornlist'} ).find_all('span')
					for actor in actores:
						casting.append(actor.string)
				except:
					pass

				pub = soup.find('div', {'class':'upload-date'}).find('li')
				publicado =  dateutil.parser.parse(pub.getText())

				tags = []
				for li in soup.find('div', {'class':'tags'}).find_all('li'):
					tags.append(li.string.strip())

				# Descargamos el thumbnail
				try:
					request_img = requests.get(
						imagen.replace('240x180','628x472'),
						stream = True
					)
				except:
					request_img = requests.get(
						imagen,
						stream = True
					)

				thumbnail = None

				# Sacamos thumbnail principal
				if request_img.status_code == 200:
					url_imagen = 'static/imagenes/porntube/%s.jpg' % video[31:]
					with open( url_imagen , 'wb') as f:
						for chunk in request_img:
							f.write(chunk)
					thumbnail = url_imagen
				

				# sacamos PREVIEWS, necesitamos loop de 40 posibles imagenes, sacar 10
				previews = []

				for n in range(0,40):
					# Creamos url
					img = imagen
					if '/' in imagen[-7:]:
						img = imagen.replace(imagen[-7:], '/%s.jpeg' % str(n))
					else:
						img = imagen.replace(imagen[-8:], '/%s.jpeg' % str(n))

					# intentamos cojer la imagen.
					prev_n = requests.get( img, stream = True )
					if prev_n.status_code == 200:
						url_prev_n = 'static/imagenes/porntube/%s-thumb-%s.jpg' % ( video[31:], str(n) )
						with open( url_prev_n, 'wb') as f:
							for chunk in prev_n:
								f.write(chunk)
						previews.append(url_prev_n)


				# Subimos video a la base de datos
				
				# excepciones chungas
				if pagina_pago == [None]: continue

				subir_video(
					previews,
					casting,
					pagina_pago,
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




