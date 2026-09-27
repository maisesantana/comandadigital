from django import forms

from restaurante.pedidos.models import Demanda, Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["mesa", "observacao"]
        labels = {
            "mesa": "Mesa",
            "observacao": "Observação",
        }


class DemandaForm(forms.ModelForm):
    class Meta:
        model = Demanda
        fields = ["item", "quantidade"]
        labels = {
            "item": "Item",
            "quantidade": "Quantidade",
        }
