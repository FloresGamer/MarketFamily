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

#CategoriaArticulo

class CategoriaArticuloListView(LoginRequiredMixin, ListView):
    model = CategoriaArticulo
    template_name = 'CategoriaArticulo/index.html'
    context_object_name = 'CategoriaArticulo'
    login_url = '/login'


class CategoriaArticuloCreateView(LoginRequiredMixin, CreateView):
    model = CategoriaArticulo
    form_class = CategoriaArticuloForm
    template_name = 'CategoriaArticulo/crear.html'
    success_url = '/CategoriaArticulo/'
    login_url = '/login'

    def form_valid(self, form):
        if form.is_valid():
            # Guarda el formulario solo si es válido
            return super().form_valid(form)
        else:
            # El formulario no es válido, vuelve a renderizar la página con errores
            return self.render_to_response(self.get_context_data(form=form))


class CategoriaArticuloUpdateView(LoginRequiredMixin, UpdateView):
    model = CategoriaArticulo
    form_class = CategoriaArticuloForm
    template_name = 'CategoriaArticulo/editar.html'
    success_url = reverse_lazy('CategoriaArticulo_listar')
    login_url = '/login'

    def get_object(self, queryset=None):
        CategoriaArticulo_id = self.kwargs['pk']
        return CategoriaArticulo.objects.get(id_categoria=CategoriaArticulo_id)
    


class CategoriaArticuloEliminarView(LoginRequiredMixin, DeleteView):
    model = CategoriaArticulo
    success_url = reverse_lazy('CategoriaArticulo_listar')
    template_name = 'CategoriaArticulo/eliminar.html'
    login_url = '/login'



#Departamento

class DepartamentoListView(LoginRequiredMixin, ListView):
    model = Departamento
    template_name = 'Departamento/index.html'
    context_object_name = 'departamentos'  
    login_url = '/login'


class DepartamentoCreateView(LoginRequiredMixin, CreateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'Departamento/crear.html'
    success_url = '/Departamento/'
    login_url = '/login'

    def form_valid(self, form):
        if form.is_valid():
            # Guarda el formulario solo si es válido
            return super().form_valid(form)
        else:
            # El formulario no es válido, vuelve a renderizar la página con errores
            return self.render_to_response(self.get_context_data(form=form))

class DepartamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'Departamento/editar.html'
    success_url = reverse_lazy('Departamento_listar')
    login_url = '/login'

    def get_object(self, queryset=None):
        Departamento_id = self.kwargs['pk']
        return Departamento.objects.get(id=Departamento_id)
    

class DepartamentoEliminarView(LoginRequiredMixin, DeleteView):
    model = Departamento
    success_url = reverse_lazy('Departamento_listar')
    template_name = 'Departamento/eliminar.html'
    login_url = '/login'


#Cargo

class CargoListView(LoginRequiredMixin, ListView):
    model = Cargo
    template_name = 'Cargo/index.html'
    context_object_name = 'cargos'
    login_url = '/login'

class CargoCreateView(LoginRequiredMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'Cargo/crear.html'
    success_url = reverse_lazy('Cargo_listar')
    login_url = '/login'

    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class CargoUpdateView(LoginRequiredMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'Cargo/editar.html'
    success_url = reverse_lazy('Cargo_listar')
    login_url = '/login'

    def get_object(self, queryset=None):
        cargo_id = self.kwargs['pk']
        return Cargo.objects.get(id=cargo_id)

class CargoEliminarView(LoginRequiredMixin, DeleteView):
    model = Cargo
    success_url = reverse_lazy('Cargo_listar')
    template_name = 'Cargo/eliminar.html'
    login_url = '/login'

#Colaborador

class ColaboradorListView(LoginRequiredMixin, ListView):
    model = Colaborador
    template_name = 'Colaborador/index.html'
    context_object_name = 'colaboradores'
    login_url = '/login'

class ColaboradorCreateView(LoginRequiredMixin, CreateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = 'Colaborador/crear.html'
    login_url = '/login'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Lógica para crear el registro en el modelo HistoricoCargo
        self.crear_historico_cargo(self.object)
        return response

    def crear_historico_cargo(self, colaborador):
        # Verificar si ya existe un historial con el mismo cargo
        ultimo_historico = HistoricoCargo.objects.filter(colaborador=colaborador).order_by('-fecha_cambio').first()
        if not ultimo_historico or ultimo_historico.cargo_anterior != colaborador.cargo:
            # Solo crear un nuevo historial si no existe o el cargo ha cambiado
            HistoricoCargo.objects.create(colaborador=colaborador, cargo_anterior=colaborador.cargo, fecha_cambio=timezone.now())

    def get_success_url(self):
        return reverse_lazy('Colaborador_listar')


class ColaboradorUpdateView(LoginRequiredMixin, UpdateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = 'Colaborador/editar.html'
    success_url = reverse_lazy('Colaborador_listar')
    login_url = '/login'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Lógica para crear el registro en el modelo HistoricoCargo
        self.crear_historico_cargo(self.object)
        return response

    def crear_historico_cargo(self, colaborador):
        # Verificar si ya existe un historial con el mismo cargo
        ultimo_historico = HistoricoCargo.objects.filter(colaborador=colaborador).order_by('-fecha_cambio').first()
        if not ultimo_historico or ultimo_historico.cargo_anterior != colaborador.cargo:
            # Solo crear un nuevo historial si no existe o el cargo ha cambiado
            HistoricoCargo.objects.create(colaborador=colaborador, cargo_anterior=colaborador.cargo, fecha_cambio=timezone.now())

class ColaboradorEliminarView(LoginRequiredMixin, DeleteView):
    model = Colaborador
    success_url = reverse_lazy('Colaborador_listar')
    template_name = 'Colaborador/eliminar.html'
    login_url = '/login'



#Sucursal

class SucursalListView(LoginRequiredMixin, ListView):
    model = Sucursal
    template_name = 'Sucursal/index.html'
    context_object_name = 'Sucursal'
    login_url = '/login'


class SucursalCreateView(LoginRequiredMixin, CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'Sucursal/crear.html'
    success_url = '/Sucursal/'
    login_url = '/login'

    def form_valid(self, form):
        if form.is_valid():
            # Guarda el formulario solo si es válido
            return super().form_valid(form)
        else:
            # El formulario no es válido, vuelve a renderizar la página con errores
            return self.render_to_response(self.get_context_data(form=form))


class SucursalUpdateView(LoginRequiredMixin, UpdateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'Sucursal/editar.html'
    success_url = reverse_lazy('Sucursal_listar')
    login_url = '/login'

    def get_object(self, queryset=None):
        Sucursal_id = self.kwargs['pk']
        return Sucursal.objects.get(id=Sucursal_id)
    


class SucursalEliminarView(LoginRequiredMixin, DeleteView):
    model = Sucursal
    success_url = reverse_lazy('Sucursal_listar')
    template_name = 'Sucursal/eliminar.html'
    login_url = '/login'



#PrecioHistorico

class PrecioHistoricoListView(LoginRequiredMixin, ListView):
    model = PrecioHistorico
    template_name = 'PrecioHistorico/index.html'
    context_object_name = 'PrecioHistorico'
    login_url = '/login'
