from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import logging


class InicioView(TemplateView):
    template_name = 'pagina/inicio.html'


#Usuarios

class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'Usuario/index.html'
    context_object_name = 'Usuarios'
    login_url = '/login'


class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'Usuario/crear.html'
    success_url = '/Usuarios/'
    login_url = '/login'

    def form_valid(self, form):
        if form.is_valid():
            # Guarda el formulario solo si es válido
            return super().form_valid(form)
        else:
            # El formulario no es válido, vuelve a renderizar la página con errores
            return self.render_to_response(self.get_context_data(form=form))


class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'Usuario/editar.html'
    success_url = reverse_lazy('Usuario_listar')
    login_url = '/login'

    def get_object(self, queryset=None):
        Usuario_id = self.kwargs['pk']
        return Usuario.objects.get(id_usuario=Usuario_id)
    


class UsuarioEliminarView(LoginRequiredMixin, DeleteView):
    model = Usuario
    success_url = reverse_lazy('Usuario_listar')
    template_name = 'Usuario/eliminar.html'
    login_url = '/login'

#Articulo

class ArticuloListView(ListView):
    model = Articulo
    template_name = 'Articulo/index.html'
    context_object_name = 'articulos'

class ArticuloCreateView(CreateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'Articulo/crear.html'
    success_url = reverse_lazy('Articulo_listar')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.crear_precio_historico(self.object)
        return response

    def crear_precio_historico(self, articulo):
        ultimo_historico = PrecioHistorico.objects.filter(articulo=articulo).order_by('-fecha').first()
        if not ultimo_historico or ultimo_historico.precio != articulo.precio:
            PrecioHistorico.objects.create(articulo=articulo, precio=articulo.precio, fecha=timezone.now())

class ArticuloUpdateView(UpdateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'Articulo/editar.html'
    success_url = reverse_lazy('Articulo_listar')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Verifica si el precio ha cambiado
        nuevo_precio = form.cleaned_data['precio']
        if nuevo_precio != self.object.precio:
            logging.debug(f"Precio cambiado para {self.object.nombre}. Antiguo: {self.object.precio}, Nuevo: {nuevo_precio}")
            self.crear_precio_historico(self.object, nuevo_precio)

        return response

class ArticuloEliminarView(DeleteView):
    model = Articulo
    success_url = reverse_lazy('Articulo_listar')
    template_name = 'Articulo/eliminar.html'