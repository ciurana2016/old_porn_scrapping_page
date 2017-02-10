import requests
import dateutil.parser

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from contenido.models import PaginaTube, Video
from acciones import subir_video, trim


class Command(BaseCommand):

	'''
		SNADBOX / TEST
		
		Cojemos 100 primeras peticiones de PORNDIG.COM 
		Este comando emula peticiones AJAX
	'''

	def handle(self, *args, **options):

		url = 'http://www.porndig.com/posts/load_more_posts'
		pagina_tube = PaginaTube.objects.get( nombre='porndig.com' )

		# Loop de las peticiones
		'''
			sin llegar a 50 peticiones ya tenemos 1000 videos
		'''
		for i in range(0, 50):

			# DATA
			payload = {
				'main_category_id':1,
				'type':'post',
				'name':'category_videos',
				'filters':{'filter_type':'date','filter_period':''},
				'category_id':{'':882},
				'offset' : i * 100 if i != 0 else 0
			}

			# Peticion y sopa
			peticion = requests.post( url, data = payload )
			respuesta = peticion.json()['data']['content']
			soup = BeautifulSoup(respuesta, 'html.parser')

			# Guardamos todos los videos HD
			lista_videos = {}

			for elemento in  soup.find_all('div',{'class':'video_item_wrapper'}):
				if 'icon-video_full_hd' in str(elemento):
					
					link = 'http://www.porndig.com' + elemento.a.get('href')

					# miramos si el video existe
					try:
						video = Video.objects.get(url_video = link)
						continue
					except Video.DoesNotExist:
						pass

					thumbnail = elemento.img.get('src').replace('320x180','400x225')
					lista_videos[link] = thumbnail
					

			# Recorremos todos los videos HD y los guardamos
			for url_video, url_thumbnail in lista_videos.iteritems():

				# Peticion y sopa
				peticion = requests.get( url_video )
				sopa = BeautifulSoup( peticion.content, 'html.parser' )

				# Todos los datos del video
				titulo = sopa.h1.text
				casting = []
				publicado = sopa.find_all('div', {'class':'video_class_value'})[3].text
				publicado = dateutil.parser.parse(publicado)

				# pagpago (si existe) y Tags
				pagina_pago, tags = [], []
				
				for elemento in sopa.find_all('div', {'class':'video_description_item'}):
					if 'Studio:' in elemento.getText():
						pagina_pago = [ elemento.a.text ]

					if 'Categories:' in elemento.getText():
						tags = [ a.text for a in elemento.find_all('a') ]

					if 'Pornstar(s)' in elemento.getText():
						casting = [ a.text for a in elemento.find_all('a') ]

				codigo_iframe = sopa.find('div',{'class':'js_video_embed'})
				codigo_iframe = codigo_iframe.textarea.iframe.get('src')

				# Intentamos sacar la pagina pago del Iframe
				if not pagina_pago:
					try:
						headers = {
							'referer' : 'http://www.porndig.com'
						}
						sopa_iframe = requests.get( codigo_iframe, headers=headers )
						sopa_iframe = BeautifulSoup( sopa_iframe.content, 'html.parser' )
						el = sopa_iframe.find('span' ,{'id':'producer_overlay_content_top_left_text'})
						pagina_pago =  [ el.a.text ] 
					except:
						pass

				# # Descargamos el thumbnail
				request_img = requests.get(url_thumbnail, stream = True )
				thumbnail = None

				if request_img.status_code == 200:
					url_imagen = 'static/imagenes/porndig/%s.jpg' % trim(titulo)
					with open( url_imagen , 'wb') as f:
						for chunk in request_img:
							f.write(chunk)
					thumbnail = url_imagen

				# Guardamos el video
				subir_video(
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

			
	
	
		print 'FIN sandbox_porndig_1'
			
	


		


