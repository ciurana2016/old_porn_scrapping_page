import operator

from random import shuffle, randint

from django.views.generic import TemplateView, DetailView, ListView
from django.shortcuts import redirect, render_to_response
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from models import Video, PaginaTube, PaginaPago, Modelo, Tag



class IndexView( TemplateView ):
	'''
		PAGINA DE INICIO
	'''
	template_name = 'index.html'

	def get_context_data(self, **kwargs):

		context = super(IndexView, self).get_context_data(**kwargs)

		# Sacamos los 20 ultimos videos de cada PaginaTube
		ultimos_videos = []

		for pagina in PaginaTube.objects.filter(activa=True):
			ultimos_videos += Video.objects.filter(
				pagina_tube=pagina).order_by('-publicado')[:40]

		# Luego los desordenamos
		shuffle( ultimos_videos )
		context['ultimos_videos'] = ultimos_videos

		return context


class VideoView( DetailView ):
	'''
		Pagina para cada video, con relacionados abajo
	'''
	model = Video
	template_name = 'video.html'

	def get_context_data(self, **kwargs):

		context = super(VideoView, self).get_context_data(**kwargs)
		video = context['object']

		# RELACIONES

		# Sacamos Actrices y sus videos
		relacion_casting = {};
		for modelo in video.casting.all():

			videos = Video.objects.filter(
				casting=modelo).order_by('-publicado')[:21]

			new_videos = [ vid for vid in videos if vid != video ]

			if new_videos:
				relacion_casting[modelo.nombre] = new_videos

		context[ 'casting' ] = relacion_casting

		# Sacamos pagina_pago y sus videos
		try:
			relacion_pago = {
				video.pagina_pago.all()[0] : []
			}

			for vid in Video.objects.filter(
				pagina_pago=video.pagina_pago.all()).order_by('-publicado')[:21]:

				if vid != video:
					relacion_pago[video.pagina_pago.all()[0]].append(vid)

			if relacion_pago[video.pagina_pago.all()[0]]:
				context[ 'pagina_pago' ] = relacion_pago

		except IndexError:
			context[ 'pagina_pago' ] = False

		# Sacamos videos relacionados segun TAGS
		tags = video.tags.all()[:4]
		relacion_tag = []

		for tag in tags:
			videos =  Video.objects.filter(tags=tag).order_by('?')[:5]

			for vid in videos:
				relacion_tag.append( vid )

		# Mzclamos
		shuffle( relacion_tag )
		context[ 'videos_relacionados' ] = relacion_tag

		return context


class VideoListView( ListView ):
	'''
		Todos los videos, por fecha, paginado, shuffled
	'''
	template_name = 'all_videos.html'
	paginate_by = 200

	def get_queryset(self):

		# No mostramos los 200 primeros ya que esos van 
		# en la HOME / IndexView
		queryset = Video.objects.all().order_by('-publicado')[200:]
		return queryset

	def get_context_data(self, **kwargs):

		context = super(VideoListView, self).get_context_data(**kwargs)

		# Randomizamos el orden de cada 200 videos
		new_list = list(context['video_list'])
		shuffle( new_list )
		context['new_list'] = new_list

		return context


class Lista( ListView ):
	''' Para paginar TAGS, MODELOS y PAGINAS PAGO '''
	template_name = 'all_list.html'
	paginate_by = 200

	def get_context_data(self, **kwargs):

		context = super(Lista, self).get_context_data(**kwargs)

		# Sacamos el nombre del modelo de object 
		# Para usarlo en template
		modelo =  context['object_list'][0].__class__.__name__
		context['modelo'] = modelo
	
		return context


class PaginaPagoListView( Lista, ListView ):
	def get_queryset(self):
		# Sacamos todas las pagina_pago
		queryset = PaginaPago.objects.all().order_by('-numero_videos')
		return queryset


class ModeloListView( Lista, ListView ):
	def get_queryset(self):
		queryset = Modelo.objects.all().order_by('-numero_videos')
		return queryset


class TagsListView( Lista, ListView ):
	def get_queryset(self):
		queryset = Tag.objects.all().order_by('-numero_videos')
		return queryset


class VideosPaginaPagoView( ListView ):
	context_object_name = 'new_list'
	template_name = 'all_videos.html'
	paginate_by = 200

	def get_queryset(self):

		paginapago = self.kwargs['paginapago']
		queryset = Video.objects.filter(
			pagina_pago__nombre_api=paginapago).order_by('-publicado')

		return queryset

	def get_context_data(self, **kwargs):

		context = super(VideosPaginaPagoView, self).get_context_data(**kwargs)

		try:
			paginapago = PaginaPago.objects.get(nombre_api=self.kwargs['paginapago'])
		except PaginaPago.DoesNotExist:
			raise Http404()

		context['nombre_modelo'] = paginapago.nombre	
		return context


class VideosModeloView( ListView ):
	context_object_name = 'new_list'
	template_name = 'all_videos.html'
	paginate_by = 200

	def get_queryset(self):

		modelo = self.kwargs['modelo']
		queryset = Video.objects.filter(
			casting__nombre_api=modelo).order_by('-publicado')

		return queryset

	def get_context_data(self, **kwargs):

		context = super(VideosModeloView, self).get_context_data(**kwargs)

		try:
			modelo = Modelo.objects.get(nombre_api=self.kwargs['modelo'])
		except Modelo.DoesNotExist:
			raise Http404()

		context['nombre_modelo'] = modelo.nombre
		return context


class VideosTagView( ListView ):
	context_object_name = 'new_list'
	template_name = 'all_videos.html'
	paginate_by = 200

	def get_queryset(self):

		tag = self.kwargs['tag']
		queryset = Video.objects.filter(
			tags__nombre_api=tag).order_by('-publicado')

		return queryset

	def get_context_data(self, **kwargs):

		context = super(VideosTagView, self).get_context_data(**kwargs)

		try:
			tag = Tag.objects.get(nombre_api=self.kwargs['tag'])
		except Tag.DoesNotExist:
			raise Http404()

		context['nombre_modelo'] = tag.nombre
		return context


# FOOTER
class AboutView( TemplateView ):
	template_name = 'about.html'

class ContactoView( TemplateView ):
	template_name = 'contacto.html'

class TosView( TemplateView ):
	template_name = 'tos.html'



#Si encuentra un 404 redirige a la home
def handler404(request):
	return redirect('http://www.meneandotela.com')


#Si peta osea un 500 que me envie el error al mail
def handler500(request):

	import sys
	ltype,lvalue,ltraceback = sys.exc_info()
	contenido = '''
		[ REQUEST : %s ]

		ERROR:
		----
		%s
		----
		%s
		----
		%s
	''' % ( request, ltype, lvalue, ltraceback )

	send_mail(
		'( meneandotela ) [ERROR: 500][%s]' % ltype,
		contenido,
		settings.EMAIL_HOST_USER,
		[settings.EMAIL_HOST_USER, 'uvesoftware@gmail.com'],
		fail_silently=False
	)

	return render_to_response('500.html')









