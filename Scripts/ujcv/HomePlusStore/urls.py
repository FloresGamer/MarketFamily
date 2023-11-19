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
    
    path('CategoriaArticulo/', CategoriaArticuloListView.as_view(), name='CategoriaArticulo_listar'),
    path('CategoriaArticulo/crear/', CategoriaArticuloCreateView.as_view(), name='CategoriaArticulo_crear'),
    path('CategoriaArticulo/<int:pk>/editar/', CategoriaArticuloUpdateView.as_view(), name='CategoriaArticulo_editar'),
    path('CategoriaArticulo/<int:pk>/eliminar/', CategoriaArticuloEliminarView.as_view(), name='CategoriaArticulo_eliminar'),

    path('Departamento/', DepartamentoListView.as_view(), name='Departamento_listar'),
    path('Departamento/crear/', DepartamentoCreateView.as_view(), name='Departamento_crear'),
    path('Departamento/<int:pk>/editar/', DepartamentoUpdateView.as_view(), name='Departamento_editar'),
    path('Departamento/<int:pk>/eliminar/', DepartamentoEliminarView.as_view(), name='Departamento_eliminar'),

    path('Cargo/', CargoListView.as_view(), name='Cargo_listar'),
    path('Cargo/crear/', CargoCreateView.as_view(), name='Cargo_crear'),
    path('Cargo/<int:pk>/editar/', CargoUpdateView.as_view(), name='Cargo_editar'),
    path('Cargo/<int:pk>/eliminar/', CargoEliminarView.as_view(), name='Cargo_eliminar'),

    path('Colaborador/', ColaboradorListView.as_view(), name='Colaborador_listar'),
    path('Colaboradores/crear/', ColaboradorCreateView.as_view(), name='Colaborador_crear'),
    path('Colaboradores/<int:pk>/editar/', ColaboradorUpdateView.as_view(), name='Colaborador_editar'),
    path('Colaboradores/<int:pk>/eliminar/', ColaboradorEliminarView.as_view(), name='Colaborador_eliminar'),
    
    path('Sucursal/', SucursalListView.as_view(), name='Sucursal_listar'),
    path('Sucursales/crear/', SucursalCreateView.as_view(), name='Sucursal_crear'),
    path('Sucursales/<int:pk>/editar/', SucursalUpdateView.as_view(), name='Sucursal_editar'),
    path('Sucursales/<int:pk>/eliminar/', SucursalEliminarView.as_view(), name='Sucursal_eliminar'),

    path('PrecioHistorico/', PrecioHistoricoListView.as_view(), name='PrecioHistorico_listar'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
