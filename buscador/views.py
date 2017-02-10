import json


from django.http import HttpResponse, Http404
from django.views.generic import TemplateView, ListView
from django.db.models import Q

from contenido.models import PaginaPago, Modelo, Tag, Video



class BuscadorView( TemplateView ):
	template_name = 'buscador.html'

	def get(self, request, *args, **kwargs):

		# Definimos lo que ha buscado el usuario
		query =  request.GET.get('q', '').replace(' ','').lower()

		# si la query es muy corta
		if len(query) < 3:
			raise Http404()

		# Miramos si la busqueda esta en algun objeto de 
		# la base de datos
		tags_q = Tag.objects.filter(nombre_api__startswith=query)
		paginas_q = PaginaPago.objects.filter(nombre_api__startswith=query)
		modelo_q = Modelo.objects.filter(nombre_api__startswith=query)

		resultados = [
			paginas_q,
			modelo_q,
			tags_q,
		]

		html_respuesta = ''

		# Creamos html para responder
		for resultado in resultados:
			if len(resultado):
				
				if resultado[0].__class__.__name__ == 'Tag':
					result_type = 'Tags'
				
				if resultado[0].__class__.__name__ == 'Modelo':
					result_type = 'Pornstars'

				if resultado[0].__class__.__name__ == 'PaginaPago':
					result_type = 'Channels'

				lis = ''
				count_lis = 0

				for r in resultado:
					count_lis += 1
					lis += '''
					<li>
					<a href="http://www.meneandotela.com/%s/%s">%s</a>
					</li>
				''' % ( result_type.lower(), r.nombre_api, r.nombre )

				type_id = result_type

				html_result_type = '''
				<div class="result_type">
				<div class="result_type_name">
				<span class="rtn" id="type_%s">%s</span>
				</div>
				<ul class="result_type_options">
					%s
				</ul>
				</div>
				''' % ( type_id.lower(), type_id, lis )

				html_respuesta += html_result_type

		# Quitamos espacions inecesarios
		html_respuesta = html_respuesta.replace('\n', '').replace('\t', '')
		data = {
			'html' : html_respuesta
		}

		if data['html']:
			return HttpResponse(json.dumps(data), content_type='application/json')
		else:
			raise Http404()


class ResultadoBusquedaView( ListView ):
	context_object_name = 'new_list'
	template_name = 'buscador.html'
	paginate_by = 200

	def get_queryset(self):

		# Que ha buscado el usuario
		query = self.request.GET.get('q', '').replace(' ','').lower()

		# si la query es muy corta
		if len(query) < 3:
			raise Http404()

		# Generamos peticion a db
		tags = Q( tags__nombre_api__startswith = query )
		pagina_pago = Q( pagina_pago__nombre_api__startswith = query )
		modelo = Q( casting__nombre_api__startswith = query )

		queryset = Video.objects.filter(
			tags | pagina_pago | modelo).order_by('-publicado').distinct()

		return queryset

	def get_context_data(self, **kwargs):

		# Que ha buscado el usuario
		query = self.request.GET.get('q', '').replace(' ','').lower()

		# url para paginator
		url_paginator = '?q='+query

		context = super( ResultadoBusquedaView, self).get_context_data(**kwargs)
		context['query'] = query
		context['url_paginator'] = url_paginator

		return context


		



















