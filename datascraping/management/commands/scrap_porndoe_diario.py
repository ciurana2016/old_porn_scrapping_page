import requests
import datetime

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from contenido.models import PaginaTube, Video
from acciones import subir_video, trim


class Command(BaseCommand):

	'''
		SCRAP DIARIO PORNDOE.COM
		
		Copia literal sandbox

		Cojemos 10 primeras peticiones de PORNDOE.COM 
		
	'''

	def handle(self, *args, **options):

		# Variables
		url_base = 'http://www.porndoe.com'
		cookies = dict(__language="en")
		pagina_tube = PaginaTube.objects.get(nombre='porndoe.com')

		''' Loop this '''
		for i in range(0, 5):

			# Peticion y sopa
			if i == 0:
				peticion = requests.get( url_base, cookies=cookies )
			else:
				peticion = requests.get( url_base+'/?page=%s' % str(i+1),
					cookies=cookies )
			soup = BeautifulSoup( peticion.content, 'html.parser' )

			# Sacamos todos los vids de la pagina
			lista_videos = {}

			for video in soup.find_all('article',{'class':'video-item'}):
				
				# Miramos si el video es HD
				if video.find('span',{'class':'ico-hd-new'}):
					link = url_base + video.a.get('href')

					# Miramos si el video existe
					try:
						v = Video.objects.get( url_video = link )
						continue
					except Video.DoesNotExist:
						pass

					thumbnail = video.img.get('src')
					lista_videos[link] = thumbnail


			# Recorremos video a video
			for url_video, url_thumbnail in lista_videos.iteritems():

				# Peticion y sopa
				peticion = requests.get( url_video, cookies=cookies )
				soup = BeautifulSoup( peticion.content, 'html.parser' )

				# Definimos variables
				titulo = soup.h1.text
				publicado = datetime.datetime.now()

				# Codigo_iframe
				c = soup.find('div', {'id':'my-embed'}).input.get('value')
				codigo_iframe = BeautifulSoup(c,'html.parser').iframe.get('src')
				
				# pagina_pago
				pagina_pago = [ soup.find('div',{'class':'channel-about'}).a.get('title') ]
				
				# Casting
				casting = [ s.text for s in soup.find_all('span',{'class':'performer-name'}) ]
				try:
					casting.remove('Suggest performer')
				except:
					pass

				# Tags
				tags = []
				for p in soup.find_all('p',{'class','data-row'}):
					if 'Tags:' in p.getText():
						tags = [ a.get('title') for a in p.find_all('a') ]


				# descargamos el thumbnail
				thumbnail = None
				peticion_img = requests.get(url_thumbnail, stream=True)

				if peticion_img.status_code == 200:
					path_imagen = 'static/imagenes/porndoe/%s.jpg' % trim(url_thumbnail)
					thumbnail = path_imagen
					with open( path_imagen , 'wb') as f:
						for chunk in peticion_img:
							f.write(chunk)


				# Sacamos previews
				previews = []

				for n in range(0, 36):
					if n % 2 != 0:
						img = url_thumbnail

						if '_' in url_thumbnail[-7:]:
							img = url_thumbnail.replace(url_thumbnail[-7:], '_%s.jpg' % str(n))
						else:
							img = url_thumbnail.replace(url_thumbnail[-8:], '_%s.jpg' % str(n))

						# intentamos cojer la imagen.
						prev_n = requests.get( img, stream = True )
						if prev_n.status_code == 200:
							url_prev_n = 'static/imagenes/porndoe/%s-thumb-%s.jpg' % ( trim(url_thumbnail), str(n) )
							with open( url_prev_n, 'wb') as f:
								for chunk in prev_n:
									f.write(chunk)
							previews.append(url_prev_n)


				# Guardamos el objeto
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
					codigo_iframe
				)				
				
			# 	break
			# break


		


