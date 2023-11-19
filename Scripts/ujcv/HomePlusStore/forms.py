from django import forms
from .models import Usuario, Articulo, CategoriaArticulo, Departamento,Cargo, Colaborador, Sucursal, PrecioHistorico
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone



class UsuarioForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date', 'value': '2000-01-01'}
        )
    )

    class Meta:
        model = Usuario
        fields = "_all_"
        widgets = {
            'contraseña': forms.PasswordInput(render_value=True),
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if any(char.isdigit() for char in nombre):
            raise forms.ValidationError("El nombre no puede contener números.")
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if any(char.isdigit() for char in apellido):
            raise forms.ValidationError("El apellido no puede contener números.")
        return apellido

    def clean_numero_telefono(self):
        numero_telefono = self.cleaned_data.get('numero_telefono')
        if any(char.isalpha() for char in numero_telefono):
            raise forms.ValidationError("El número de teléfono no puede contener letras.")
        return numero_telefono

    def clean_all_fields(self):
        for field_name, field_value in self.cleaned_data.items():
            if isinstance(field_value, str) and len(field_value) < 10:
                raise forms.ValidationError(f"El campo {self.fields[field_name].label} debe contener al menos 10 caracteres.")
        return self.cleaned_data
    
    def clean_documento_identidad(self):
        documento_identidad = self.cleaned_data.get('documento_identidad')
        if not documento_identidad:
            raise forms.ValidationError("El documento de identidad es obligatorio. Por favor, sube un documento.")
        return documento_identidad
    
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        fecha_minima = date(1920, 1, 1)
        fecha_actual = date.today()
        edad_minima = 18

        if fecha_nacimiento < fecha_minima or fecha_nacimiento > fecha_actual:
            raise forms.ValidationError(
                'La fecha de nacimiento debe estar entre el 1 de enero de 1920 y la fecha actual.'
            )

        edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        if edad < edad_minima:
            raise forms.ValidationError(
                f'Debes ser mayor de {edad_minima} años para registrarte.'
            )

        return fecha_nacimiento


class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = "_all_"

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if not imagen:
            raise forms.ValidationError("La imagen del artículo es obligatoria. Por favor, sube una imagen.")
        return imagen

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 500:
            raise forms.ValidationError("El precio del artículo no puede ser menor de 500.")
        return precio

    def save(self, commit=True):
        articulo = super().save(commit)
        
        # Registra el precio en el historial
        PrecioHistorico.objects.create(articulo=articulo, precio=articulo.precio, fecha=timezone.now())
        
        return articulo
    
class CategoriaArticuloForm(forms.ModelForm):
    class Meta:
        model = CategoriaArticulo
        fields = "_all_"

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = "_all_"



class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = "_all_"

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if any(char.isdigit() for char in nombre):
            raise forms.ValidationError("El nombre no puede contener números.")
        return nombre

    def clean_sueldo(self):
        sueldo = self.cleaned_data.get('sueldo')
        # Asegúrate de que el sueldo sea mayor o igual a 8000
        if sueldo < 8000:
            raise forms.ValidationError("El sueldo debe ser igual o mayor a 8000.")
        return sueldo


class ColaboradorForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date', 'value': '2000-01-01'}
        )
    )

    class Meta:
        model = Colaborador
        fields = '_all_'
        widgets = {
            'contraseña': forms.PasswordInput(render_value=True),
        }

    def clean_perfil(self):
        perfil = self.cleaned_data.get('perfil')
        if not perfil:
            raise forms.ValidationError("La foto de perfil es obligatoria. Por favor, sube una imagen.")
        return perfil
    
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        fecha_minima = date(1920, 1, 1)
        fecha_actual = date.today()
        edad_minima = 18

        if fecha_nacimiento < fecha_minima or fecha_nacimiento > fecha_actual:
            raise forms.ValidationError(
                'La fecha de nacimiento debe estar entre el 1 de enero de 1920 y la fecha actual.'
            )

        edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        if edad < edad_minima:
            raise forms.ValidationError(
                f'Debes ser mayor de {edad_minima} años para registrarte.'
            )

        return fecha_nacimiento
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        # Excluir la opción 'cliente' del queryset del campo 'rol'
        self.fields['rol'].queryset = self.fields['rol'].queryset.exclude(nombre='cliente')

class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = "_all_"
        widgets = {
            'hora_apertura': forms.TimeInput(attrs={'type': 'time'}),
            'hora_cierre': forms.TimeInput(attrs={'type': 'time'}),
            'fecha_inauguracion': forms.DateInput(attrs={'type': 'date'}),
        }

class PrecioHistoricoForm(forms.ModelForm):
    class Meta:
        model = PrecioHistorico
        fields = "_all_"