# Generated by Django 4.2.7 on 2023-11-18 02:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('HomePlusStore', '0003_cargo_departamento_documentopersonal_colaborador'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('hora_apertura', models.TimeField()),
                ('hora_cierre', models.TimeField()),
                ('direccion', models.TextField()),
                ('fecha_inauguracion', models.DateField()),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id_inventario', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad_disponible', models.PositiveIntegerField()),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HomePlusStore.articulo')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HomePlusStore.sucursal')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricoCargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_cambio', models.DateTimeField(default=django.utils.timezone.now)),
                ('cargo_anterior', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HomePlusStore.cargo')),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HomePlusStore.colaborador')),
            ],
        ),
    ]
