from django.urls import path

from restaurante.cardapio.views import (
    cardapio_list,
    categoria_create,
    categoria_delete,
    categoria_update,
    item_create,
    item_delete,
    item_list,
    item_toggle_disponibilidade,
    item_update,
)

urlpatterns = [
    path("", cardapio_list, name="cardapio_list"),
    path("categorias/nova/", categoria_create, name="categoria_create"),
    path("categorias/<int:pk>/editar/",
         categoria_update, name="categoria_update"),
    path("categorias/<int:pk>/excluir/",
         categoria_delete, name="categoria_delete"),
    path("itens/", item_list, name="item_list"),
    path("itens/novo/", item_create, name="item_create"),
    path("itens/<int:pk>/editar/", item_update, name="item_update"),
    path("itens/<int:pk>/excluir/", item_delete, name="item_delete"),
    path("itens/<int:pk>/toggle-disponibilidade/",
         item_toggle_disponibilidade, name="item_toggle_disponibilidade"),
]
