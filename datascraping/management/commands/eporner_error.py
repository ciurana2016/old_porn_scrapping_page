
'''

	ERA PARA PROBAR UN ERROR , EL CUAL CREO QUE YA NO EXISTE

	no se guardaba uno de los videos en pagina_pago = blacked y el otro si
	pero ahora ya funciona
'''

import requests
import datetime

from bs4 import BeautifulSoup
from acciones import subir_video
from contenido.models import PaginaTube


video_malo = 'http://www.eporner.com/hd-porn/597606/Blacked-Blonde-Babysitter-Trillium-Fucks-Her-Black-Boss/'
video_bueno = 'http://www.eporner.com/hd-porn/591814/Blacked-Blonde-Teen-Dakota-James-First-Experience-With-Big-Black-Cock/'

pagina_tube = PaginaTube.objects.get( nombre="eporner.com" )

# Peticion y sopa
peticion = requests.get( video_malo )
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
# request_img = requests.get(url_thumbnail, stream = True )
thumbnail = None

# if request_img.status_code == 200:
# 	url_imagen = 'static/imagenes/eporner/%s.jpg' % trim(titulo)
# 	with open( url_imagen , 'wb') as f:
# 		for chunk in request_img:
# 			f.write(chunk)
# 	thumbnail = url_imagen

# Guardamos el objeto
subir_video(
	cast,
	[],
	pagina_tube,
	tags,
	titulo,
	thumbnail,
	publicado,
	video_malo,
	codigo_iframe,
)
	

print 'FIN '