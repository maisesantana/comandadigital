from django.urls import path

from restaurante.pedidos.views import (
    cozinha_list,
    demanda_avancar,
    demanda_cancelar,
    pedido_cancelar,
    pedido_create,
    pedido_detail,
    pedido_fechar,
    pedido_list,
)

urlpatterns = [
    path("", pedido_list, name="pedido_list"),
    path("novo/", pedido_create, name="pedido_create"),
    path("<int:pk>/", pedido_detail, name="pedido_detail"),
    path("<int:pk>/cancelar/", pedido_cancelar, name="pedido_cancelar"),
    path("<int:pk>/fechar/", pedido_fechar, name="pedido_fechar"),
    path("demandas/<int:pk>/avancar/", demanda_avancar, name="demanda_avancar"),
    path("demandas/<int:pk>/cancelar/",
         demanda_cancelar, name="demanda_cancelar"),
    path("cozinha/", cozinha_list, name="cozinha_list"),
]
