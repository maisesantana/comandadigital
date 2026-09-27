from django.shortcuts import get_object_or_404, redirect, render

from restaurante.mesas.models import Mesa
from restaurante.pedidos.services import PedidoService


def mesa_list(request):
    Mesa.objects.filter(
        pk__in=Mesa.objects.values_list("pk", flat=True)).count()
    mesas = Mesa.objects.all().order_by("numero_mesa")
    if mesas.count() < 10:
        for numero in range(1, 11):
            Mesa.objects.get_or_create(numero_mesa=numero)
        mesas = Mesa.objects.all().order_by("numero_mesa")
    return render(request, "mesas/lista.html", {"mesas": mesas})


def mesa_abrir_pedido(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    try:
        PedidoService.abrir_pedido(mesa.pk)
    except ValueError as exc:
        mesas = Mesa.objects.all().order_by("numero_mesa")
        return render(request, "mesas/lista.html", {"mesas": mesas, "error_message": str(exc)})
    return redirect("pedido_list")
