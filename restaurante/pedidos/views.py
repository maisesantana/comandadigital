from django.shortcuts import get_object_or_404, redirect, render

from restaurante.cardapio.models import Item
from restaurante.pedidos.forms import DemandaForm, PedidoForm
from restaurante.pedidos.models import Demanda, Pedido
from restaurante.pedidos.services import PedidoService


def pedido_list(request):
    pedidos = Pedido.objects.select_related(
        "mesa").all().order_by("-data_hora")
    return render(request, "pedidos/lista.html", {"pedidos": pedidos})


def pedido_detail(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    demandas = pedido.demandas.select_related(
        "item").all().order_by("data_hora")
    form = DemandaForm(request.POST or None, initial={"pedido": pedido})
    form.fields["item"].queryset = Item.objects.filter(disponivel=True)
    if request.method == "POST" and form.is_valid():
        try:
            PedidoService.adicionar_demanda(
                pedido.pk, form.cleaned_data["item"].pk, form.cleaned_data["quantidade"])
            return redirect("pedido_detail", pk=pedido.pk)
        except ValueError as exc:
            return render(request, "pedidos/detalhe.html", {"pedido": pedido, "demandas": demandas, "form": form, "error_message": str(exc)})
    return render(request, "pedidos/detalhe.html", {"pedido": pedido, "demandas": demandas, "form": form})


def pedido_create(request):
    form = PedidoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            pedido = PedidoService.abrir_pedido(form.cleaned_data["mesa"].pk)
            return redirect("pedido_detail", pk=pedido.pk)
        except ValueError as exc:
            return render(request, "pedidos/formulario.html", {"form": form, "error_message": str(exc)})
    return render(request, "pedidos/formulario.html", {"form": form})


def pedido_cancelar(request, pk):
    try:
        PedidoService.cancelar_pedido(pk)
    except ValueError as exc:
        pedidos = Pedido.objects.select_related(
            "mesa").all().order_by("-data_hora")
        return render(request, "pedidos/lista.html", {"pedidos": pedidos, "error_message": str(exc)})
    return redirect("pedido_list")


def pedido_fechar(request, pk):
    try:
        PedidoService.fechar_pedido(pk)
    except ValueError as exc:
        pedido = get_object_or_404(Pedido, pk=pk)
        demandas = pedido.demandas.select_related(
            "item").all().order_by("data_hora")
        form = DemandaForm(initial={"pedido": pedido})
        form.fields["item"].queryset = Item.objects.filter(disponivel=True)
        return render(request, "pedidos/detalhe.html", {"pedido": pedido, "demandas": demandas, "form": form, "error_message": str(exc)})
    return redirect("pedido_list")


def demanda_avancar(request, pk):
    demanda = get_object_or_404(Demanda, pk=pk)
    try:
        PedidoService.avancar_demanda(demanda.pk)
    except ValueError as exc:
        pedido = demanda.pedido
        demandas = pedido.demandas.select_related(
            "item").all().order_by("data_hora")
        form = DemandaForm(initial={"pedido": pedido})
        form.fields["item"].queryset = Item.objects.filter(disponivel=True)
        return render(request, "pedidos/detalhe.html", {"pedido": pedido, "demandas": demandas, "form": form, "error_message": str(exc)})
    return redirect("pedido_detail", pk=demanda.pedido.pk)


def demanda_cancelar(request, pk):
    demanda = get_object_or_404(Demanda, pk=pk)
    try:
        PedidoService.cancelar_demanda(demanda.pk)
    except ValueError as exc:
        pedido = demanda.pedido
        demandas = pedido.demandas.select_related(
            "item").all().order_by("data_hora")
        form = DemandaForm(initial={"pedido": pedido})
        form.fields["item"].queryset = Item.objects.filter(disponivel=True)
        return render(request, "pedidos/detalhe.html", {"pedido": pedido, "demandas": demandas, "form": form, "error_message": str(exc)})
    return redirect("pedido_detail", pk=demanda.pedido.pk)


def cozinha_list(request):
    demandas = Demanda.objects.select_related("pedido__mesa", "item").filter(
        status__in=[Demanda.STATUS_PENDENTE, Demanda.STATUS_EM_PREPARO]).order_by("data_hora")
    return render(request, "cozinha/lista.html", {"demandas": demandas})
