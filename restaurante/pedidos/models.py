from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model

from restaurante.cardapio.models import Item
from restaurante.mesas.models import Mesa


class Pedido(Model):
    STATUS_ABERTO = "aberto"
    STATUS_FECHADO = "fechado"
    STATUS_CANCELADO = "cancelado"
    STATUS_CHOICES = [
        (STATUS_ABERTO, "Aberto"),
        (STATUS_FECHADO, "Fechado"),
        (STATUS_CANCELADO, "Cancelado"),
    ]

    mesa = models.ForeignKey(
        Mesa, on_delete=models.PROTECT, related_name="pedidos", verbose_name="mesa")
    data_hora = models.DateTimeField(
        auto_now_add=True, verbose_name="data e hora")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_ABERTO, verbose_name="status")
    valor_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="valor total")
    observacao = models.TextField(
        blank=True, default="", verbose_name="observação")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        constraints = [
            models.UniqueConstraint(
                fields=["mesa"],
                condition=models.Q(status="aberto"),
                name="unique_open_pedido_per_mesa",
            )
        ]

    def __str__(self):
        return f"Pedido {self.pk} - Mesa {self.mesa.numero_mesa}"


class Demanda(Model):
    STATUS_PENDENTE = "pendente"
    STATUS_EM_PREPARO = "em preparo"
    STATUS_FINALIZADA = "finalizada"
    STATUS_CANCELADA = "cancelada"
    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_EM_PREPARO, "Em preparo"),
        (STATUS_FINALIZADA, "Finalizada"),
        (STATUS_CANCELADA, "Cancelada"),
    ]

    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="demandas", verbose_name="pedido")
    item = models.ForeignKey(Item, on_delete=models.PROTECT,
                             related_name="demandas", null=True, blank=True, verbose_name="item")
    nome_item_snapshot = models.CharField(
        max_length=150, verbose_name="nome do item no momento da criação")
    quantidade = models.PositiveIntegerField(verbose_name="quantidade")
    preco_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="preço unitário")
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="subtotal")
    data_hora = models.DateTimeField(
        auto_now_add=True, verbose_name="data e hora")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default=STATUS_PENDENTE, verbose_name="status")

    class Meta:
        verbose_name = "Demanda"
        verbose_name_plural = "Demandas"

    def clean(self):
        super().clean()
        if self.quantidade <= 0:
            raise ValidationError(
                {"quantidade": "A quantidade deve ser positiva."})

    def save(self, *args, **kwargs):
        if self.quantidade and self.preco_unitario:
            self.subtotal = Decimal(self.quantidade) * self.preco_unitario
            if self.status == self.STATUS_CANCELADA:
                self.subtotal = Decimal("0.00")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_item_snapshot} ({self.quantidade})"
