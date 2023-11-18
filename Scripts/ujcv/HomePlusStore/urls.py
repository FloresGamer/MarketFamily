from django.urls import path
from django.contrib.staticfiles.views import serve
from .views import * 

from django.conf import settings
from django.contrib.staticfiles.urls import static


urlpatterns = [
    path('static/<path:path>', serve),
    path('', InicioView.as_view(), name='inicio'),

    path('Usuarios/', UsuarioListView.as_view(), name='Usuario_listar'),
    path('Usuarios/crear/', UsuarioCreateView.as_view(), name='Usuario_crear'),
    path('Usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='Usuario_editar'),
    path('Usuarios/<int:pk>/eliminar/', UsuarioEliminarView.as_view(), name='Usuario_eliminar'),

    path('Articulo/', ArticuloListView.as_view(), name='Articulo_listar'),
    path('Articulo/crear/', ArticuloCreateView.as_view(), name='Articulo_crear'),
    path('Articulo/<int:pk>/editar/', ArticuloUpdateView.as_view(), name='Articulo_editar'),
    path('Articulo/<int:pk>/eliminar/', ArticuloEliminarView.as_view(), name='Articulo_eliminar'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)