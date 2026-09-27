from django.urls import path

from restaurante.mesas.views import mesa_abrir_pedido, mesa_list

urlpatterns = [
    path("", mesa_list, name="mesa_list"),
    path("<int:pk>/abrir-pedido/", mesa_abrir_pedido, name="mesa_abrir_pedido"),
]
