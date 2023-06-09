# Generated by Django 4.2.1 on 2023-06-28 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_departamento_ciudad_dep_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamento',
            name='ciudad_dep',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='descripcion_dep',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='direccion_dep',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='inventario_dep',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='nombre_dep',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='valordiario_dep',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
