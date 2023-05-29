from django.contrib import admin
from . import models, forms
# Register your models here.

class ImagenDepartamentoAdmin(admin.TabularInline):
    model = models.ImagenDepartamento

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ["nombre_dep","valordiario_dep","estado_dep"]
    form = forms.DepartamentoForm
    inlines = [
        ImagenDepartamentoAdmin
    ]


admin.site.register(models.Departamento, DepartamentoAdmin)
admin.site.register(models.Reserva)
admin.site.register(models.Contacto)
admin.site.register(models.Clientes)
admin.site.register(models.Tour)
admin.site.register(models.ServiciosExtra)
