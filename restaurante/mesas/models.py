from django.db import models
from django.db.models import Model


class Mesa(Model):
    STATUS_LIVRE = "livre"
    STATUS_OCUPADA = "ocupada"
    STATUS_CHOICES = [
        (STATUS_LIVRE, "Livre"),
        (STATUS_OCUPADA, "Ocupada"),
    ]

    numero_mesa = models.PositiveIntegerField(
        unique=True, verbose_name="número da mesa")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_LIVRE,
        verbose_name="status",
    )

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"

    def __str__(self):
        return f"Mesa {self.numero_mesa}"
