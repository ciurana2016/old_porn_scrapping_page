import re
import string

from random import randint

from django.core.exceptions import ObjectDoesNotExist

from contenido.models import Modelo, PaginaTube, PaginaPago, Tag, Video, Preview


def trim(string):
	r = re.compile('[\W_]+')
	return r.sub('', string) + str(randint(0,999999))

'''
	Function que comproueva los datos del video,
	de ser necesario crea tags modelos o paginas de pago 
	y al final crea el objeto de video y lo guarda
'''
def subir_video(
	previews,
	casting,
	pagina_pago,
	pagina_tube,
	tags,
	titulo,
	thumbnail,
	publicado = False,
	url_video = '',
	codigo_iframe = '',
	):


	def nombre_api(texto):
		return texto.replace(' ','').lower()

	def network(texto):
		# Quitamos la palabra "network" para evitar crear 
		# Brazzers y Brazzers Network por ejemplo
		if 'network' in nombre_api(texto):
			texto = texto.replace('Network','').replace('network','')
		return texto

	# Creamos casting de no existir
	for cast in casting:
		if cast:
			try:
				modelo = Modelo.objects.get( nombre_api = nombre_api(cast) )
			except Modelo.DoesNotExist:
				modelo = Modelo()
				modelo.nombre = cast
				if thumbnail != None: modelo.thumbnail = thumbnail
				modelo.save()

	# Creamos pagina pago de no existir
	for pag_pago in pagina_pago:
		if pag_pago:

			pag_pago = network(pag_pago)
			try:
				paginapago = PaginaPago.objects.get( nombre_api = nombre_api(pag_pago) )
			except PaginaPago.DoesNotExist:
				paginapago = PaginaPago()
				paginapago.nombre = pag_pago
				if thumbnail != None: paginapago.thumbnail = thumbnail
				paginapago.save()

	# Hacemos lo mismo para Tags
	for tag in tags:
		if tag and len(tag) >= 3:

			tag = network(tag)
			try:
				paginapago = PaginaPago.objects.get( nombre_api = nombre_api(tag) )

			except PaginaPago.DoesNotExist:
				try:
					tag = Tag.objects.get( nombre_api = nombre_api(tag) )
				except Tag.DoesNotExist:
					tag_ = Tag()
					tag_.nombre = tag
					if thumbnail != None: tag_.thumbnail = thumbnail
					tag_.save()


	# Ahora si creamos el video
	# Se supone que se ah comprovado antes de la funcion 
	# si el video existe o no
	video = Video()
	video.titulo = titulo
	video.publicado = publicado
	video.pagina_tube = pagina_tube
	if url_video != '': video.url_video = url_video
	if codigo_iframe != '': video.codigo_iframe = codigo_iframe
	if thumbnail != None: video.thumbnail = thumbnail

	# Gaurdado inicial
	video.save()

	# A guardar los MTM
	for cast in casting:
		if cast:
			m = Modelo.objects.get( nombre_api = nombre_api(cast) )
			video.casting.add(m)

			# Anyadimos +1 al numero de videos de este CAST
			m.numero_videos += 1
			m.save()
	
	for pag_pago in pagina_pago:
		if pag_pago:
			pag_pago = network(pag_pago)
			pp = PaginaPago.objects.get( nombre_api = nombre_api(pag_pago) )
			video.pagina_pago.add(pp)

			# Anyadimos +1 al numero de videos de esta Pagina Pago
			pp.numero_videos += 1
			pp.save()

	for tag in tags:
		if tag and len(tag) >= 3:
			try:
				t = Tag.objects.get( nombre_api = nombre_api(tag) )
				video.tags.add(t)

				# Anyadimos +1 al numero de videos de este Tag
				t.numero_videos += 1
				t.save()

			# Si el tag no existe es una pagina de pago
			except Tag.DoesNotExist:
				tag = network(tag)
				pp = PaginaPago.objects.get( nombre_api = nombre_api(tag) )
				video.pagina_pago.add(pp)

				# Anyadimos +1 al numero de videos de esta Pagina Pago
				pp.numero_videos += 1
				pp.save()

	# Previews
	for preview in previews:
		if preview:
			p = Preview(img = preview)
			p.save()
			
			video.previews.add(p)

	# Guardado final
	video.save()

# FIN funcion subir_video()    por ahora




