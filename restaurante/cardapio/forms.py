from django import forms

from restaurante.cardapio.models import Categoria, Item


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome_categoria"]
        labels = {
            "nome_categoria": "Nome da categoria",
        }
        widgets = {
            "nome_categoria": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome da categoria"}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["nome_item", "preco", "categoria", "disponivel"]
        labels = {
            "nome_item": "Nome do item",
            "preco": "Preço",
            "categoria": "Categoria",
            "disponivel": "Disponível",
        }
        widgets = {
            "nome_item": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome do item"}),
            "preco": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "disponivel": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ItemDisponibilidadeForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["disponivel"]
        labels = {"disponivel": "Disponível"}
        widgets = {"disponivel": forms.CheckboxInput(
            attrs={"class": "form-check-input"})}
