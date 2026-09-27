from django.contrib import admin

from restaurante.cardapio.models import Categoria, Item


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome_categoria",)
    search_fields = ("nome_categoria",)
    ordering = ("nome_categoria",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("nome_item", "categoria", "preco", "disponivel")
    list_filter = ("categoria", "disponivel")
    search_fields = ("nome_item", "categoria__nome_categoria")
    ordering = ("categoria__nome_categoria", "nome_item")
