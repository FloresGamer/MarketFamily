from django.contrib import admin
from HomePlusStore.models import (Usuario, Articulo, CategoriaArticulo, Departamento,Cargo, Colaborador, Sucursal, PrecioHistorico)

admin.site.register(Usuario)
admin.site.register(Articulo)
admin.site.register(CategoriaArticulo)
admin.site.register(Departamento)
admin.site.register(Cargo)
admin.site.register(Colaborador)
admin.site.register(Sucursal)
admin.site.register(PrecioHistorico)
# Register your models here.
