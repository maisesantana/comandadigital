from django.contrib import admin

from restaurante.pedidos.models import Demanda, Pedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("pk", "mesa", "status", "valor_total", "data_hora")
    list_filter = ("status", "mesa")
    search_fields = ("mesa__numero_mesa", "observacao")
    ordering = ("-data_hora",)


@admin.register(Demanda)
class DemandaAdmin(admin.ModelAdmin):
    list_display = ("pk", "pedido", "nome_item_snapshot",
                    "quantidade", "status", "subtotal")
    list_filter = ("status", "pedido__mesa")
    search_fields = ("nome_item_snapshot", "pedido__mesa__numero_mesa")
    ordering = ("-data_hora",)
