from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.cache import cache_page

from contenido.views import *
from buscador.views import BuscadorView, ResultadoBusquedaView

urlpatterns = patterns('',
    
    #Pagina
    url(r'^$', cache_page(60 * 60 * 24)(IndexView.as_view()), name='index'),
    url(r'^video/(?P<slug>[_\w]+)/$', cache_page(60 * 60 * 24)(VideoView.as_view()), name='pagina_video'),
    url(r'^videos/$', VideoListView.as_view(), name='videos'),
    url(r'^channels/$', PaginaPagoListView.as_view(), name='paginas_pago'),
    url(r'^pornstars/$', ModeloListView.as_view(), name='modelos'),
    url(r'^tags/$', TagsListView.as_view(), name='tags'),

    # subd de las listas, Tags Modelos y PaginasPago
    url(r'^channels/(?P<paginapago>[^?]+)/$', VideosPaginaPagoView.as_view(), name='videos_pagina_pago'),
    url(r'^pornstars/(?P<modelo>[^?]+)/$', VideosModeloView.as_view(), name='videos_modelo'),
    url(r'^tags/(?P<tag>[^?]+)/$', VideosTagView.as_view(), name='videos_tag'),

    # Buscador ( cacheando el resultado de cada busqueda un dia)
    url(r'^search/$', cache_page(60 * 60 * 24)(BuscadorView.as_view()) ),
    url(r'^searchresults/$', cache_page(60 * 60 * 24)(ResultadoBusquedaView.as_view()) ),

    # Footer
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^contact/$', ContactoView.as_view(), name='contacto'),
    url(r'^tos/$', TosView.as_view(), name='tos'),

    #Admin
    url(r'^r2d2c3po/', include(admin.site.urls)),
)
