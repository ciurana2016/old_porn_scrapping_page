import re
import string

from random import randint

from django.db import models


class Modelo(models.Model):

	'''
		Actriz o actor porno con imagen
	'''

	nombre = models.CharField( max_length = 40 )
	nombre_api = models.CharField( max_length = 40, blank = True )
	numero_videos = models.IntegerField( default=0 )
	thumbnail = models.CharField( max_length = 120,
		default = 'static/imagenes/nothumb.png' )

	def __unicode__(self):
		return self.nombre

	def save(self, *args, **kwargs):
		self.nombre_api = self.nombre.replace(' ','').lower()
		super( Modelo, self ).save(*args, **kwargs)



class PaginaTube(models.Model):

	'''
		Ej : BEEG
	'''

	nombre = models.CharField( max_length = 40 )
	imagen = models.ImageField(
		upload_to = 'static/paginatube/',
		default = 'static/noimg.png' )

	activa = models.BooleanField( default = True )

	def __unicode__(self):
		return self.nombre


class PaginaPago(models.Model):

	'''
		Ej: BRAZZERS
	'''

	nombre = models.CharField( max_length = 40 )
	nombre_api = models.CharField( max_length = 40, blank = True )
	numero_videos = models.IntegerField( default=0 )
	thumbnail = models.CharField( max_length = 120,
		default = 'static/imagenes/nothumb.png' )

	def __unicode__(self):
		return self.nombre

	def save(self, *args, **kwargs):
		self.nombre_api = self.nombre.replace(' ','').lower()
		super( PaginaPago, self ).save(*args, **kwargs)


class Tag(models.Model):

	'''
		Tags para categorizar videos
	'''

	nombre = models.CharField( max_length = 20 )
	nombre_api = models.CharField( max_length = 20, blank = True )
	numero_videos = models.IntegerField( default=0 )
	thumbnail = models.CharField( max_length = 120,
		default = 'static/imagenes/nothumb.png' )

	def __unicode__(self):
		return self.nombre

	def save(self, *args, **kwargs):
		self.nombre_api = self.nombre.replace(' ','').lower()
		super( Tag, self ).save(*args, **kwargs)


def trim(string):
	r = re.compile('[\W_]+')
	return r.sub('', string) + str(randint(0,999999))


class Preview(models.Model):

	'''
		Imagen de vista previa a un video, vamos a poner 10 por video,
		aunque algunas paginas tienen mas de 10, para que todas sean iguales.
	'''

	img = models.CharField( max_length = 120,
		default = 'static/imagenes/nothumb.png' )

	def __unicode__(self):
		return self.img


class Video(models.Model):

	'''
		Modelo principal de la pagina
	'''

	casting = models.ManyToManyField( 'Modelo', null = True )
	codigo_iframe = models.CharField( max_length = 300, blank = True, null = True )
	pagina_pago = models.ManyToManyField( 'PaginaPago', null=True )
	pagina_tube = models.ForeignKey( 'PaginaTube', null=True, blank=True)
	publicado = models.DateTimeField( null = True )
	tags = models.ManyToManyField( 'Tag', null = True )
	titulo = models.CharField( max_length = 70 )
	thumbnail = models.CharField( max_length = 120,
		default = 'static/imagenes/nothumb.png' )
	url_video = models.CharField( max_length = 300, blank = True, null = True )
	slug = models.SlugField(max_length = 70, default='', editable=False, blank=True)

	# Nueva edicion
	previews = models.ManyToManyField( 'Preview', null = True )

	def __unicode__(self):
		return self.titulo

	def save(self, *args, **kwargs):
 		self.slug = trim(self.titulo)
		super(Video, self).save(*args, **kwargs)



