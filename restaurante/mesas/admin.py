from django.contrib import admin

from restaurante.mesas.models import Mesa


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ("numero_mesa", "status")
    list_filter = ("status",)
    search_fields = ("numero_mesa",)
    ordering = ("numero_mesa",)
