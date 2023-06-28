# Generated by Django 4.2.1 on 2023-06-28 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_contacto_avisos_remove_serviciosextra_reseñas_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamento',
            name='ciudad_dep',
            field=models.CharField(max_length=50, null=True, verbose_name='Cuidad'),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='descripcion_dep',
            field=models.TextField(verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='direccion_dep',
            field=models.CharField(max_length=50, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='inventario_dep',
            field=models.TextField(verbose_name='Inventario'),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='nombre_dep',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre departamento'),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='valordiario_dep',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor diario'),
        ),
    ]
