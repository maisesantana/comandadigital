from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model


class Categoria(Model):
    nome_categoria = models.CharField(
        max_length=100, unique=True, verbose_name="nome da categoria")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome_categoria


class Item(Model):
    nome_item = models.CharField(max_length=150, verbose_name="nome do item")
    preco = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="preço")
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="itens",
        verbose_name="categoria",
    )
    disponivel = models.BooleanField(default=True, verbose_name="disponível")

    class Meta:
        verbose_name = "Item do cardápio"
        verbose_name_plural = "Itens do cardápio"

    def clean(self):
        super().clean()
        if self.preco < Decimal("0.00"):
            raise ValidationError({"preco": "O preço não pode ser negativo."})

    def __str__(self):
        return self.nome_item
