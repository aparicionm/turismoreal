from django.contrib import admin
from . import models, forms
# Register your models here.

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ["nombre_dep","valordiario_dep","estado_dep"]
    form = forms.DepartamentoForm


admin.site.register(models.Departamento, DepartamentoAdmin)
admin.site.register(models.Reserva)
admin.site.register(models.Contacto)