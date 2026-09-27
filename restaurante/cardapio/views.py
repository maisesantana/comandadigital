from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from restaurante.cardapio.forms import CategoriaForm, ItemDisponibilidadeForm, ItemForm
from restaurante.cardapio.models import Categoria, Item


def cardapio_list(request):
    categorias = Categoria.objects.prefetch_related("itens").all()
    return render(request, "cardapio/lista.html", {"categorias": categorias})


def categoria_create(request):
    form = CategoriaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("cardapio_list")
    return render(request, "cardapio/form_categoria.html", {"form": form, "titulo": "Nova categoria"})


def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("cardapio_list")
    return render(request, "cardapio/form_categoria.html", {"form": form, "titulo": "Editar categoria"})


def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    try:
        categoria.delete()
    except ValidationError as exc:
        categorias = Categoria.objects.prefetch_related("itens").all()
        return render(request, "cardapio/lista.html", {"categorias": categorias, "error_message": str(exc)})
    return redirect("cardapio_list")


def item_list(request):
    itens = Item.objects.select_related("categoria").all()
    return render(request, "cardapio/itens.html", {"itens": itens})


def item_create(request):
    form = ItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("item_list")
    return render(request, "cardapio/form_item.html", {"form": form, "titulo": "Novo item"})


def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("item_list")
    return render(request, "cardapio/form_item.html", {"form": form, "titulo": "Editar item"})


def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    try:
        item.delete()
    except ValidationError as exc:
        itens = Item.objects.select_related("categoria").all()
        return render(request, "cardapio/itens.html", {"itens": itens, "error_message": str(exc)})
    return redirect("item_list")


def item_toggle_disponibilidade(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.disponivel = not item.disponivel
    item.save(update_fields=["disponivel"])
    return redirect("item_list")
