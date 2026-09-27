from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cardapio/", include("restaurante.cardapio.urls")),
    path("mesas/", include("restaurante.mesas.urls")),
    path("pedidos/", include("restaurante.pedidos.urls")),
    path("cozinha/", include("restaurante.pedidos.urls")),
]
