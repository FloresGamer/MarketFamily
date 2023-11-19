from django.contrib import admin
from HomePlusStore.models import (Usuario, Articulo, CategoriaArticulo, Departamento,Cargo)

admin.site.register(Usuario)
admin.site.register(Articulo)
admin.site.register(CategoriaArticulo)
admin.site.register(Departamento)
admin.site.register(Cargo)
# Register your models here.
