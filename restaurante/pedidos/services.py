from decimal import Decimal

from django.db import transaction

from restaurante.cardapio.models import Item
from restaurante.mesas.models import Mesa
from restaurante.pedidos.models import Demanda, Pedido


class PedidoService:
    @staticmethod
    def recalcular_total(pedido):
        total = Decimal("0.00")
        for demanda in pedido.demandas.all():
            if demanda.status != Demanda.STATUS_CANCELADA:
                total += demanda.subtotal
        pedido.valor_total = total
        pedido.save(update_fields=["valor_total"])

    @staticmethod
    @transaction.atomic
    def abrir_pedido(mesa_id):
        mesa = Mesa.objects.get(pk=mesa_id)
        if mesa.status == Mesa.STATUS_OCUPADA:
            raise ValueError(
                "Mesa ocupada. Não é possível abrir um novo pedido.")

        if Pedido.objects.filter(mesa=mesa, status=Pedido.STATUS_ABERTO).exists():
            raise ValueError("Já existe um pedido aberto para esta mesa.")

        if Mesa.objects.filter(status=Mesa.STATUS_OCUPADA).count() >= 10:
            raise ValueError(
                "As 10 mesas já estão ocupadas. Aguarde uma liberação.")

        pedido = Pedido.objects.create(mesa=mesa, status=Pedido.STATUS_ABERTO)
        mesa.status = Mesa.STATUS_OCUPADA
        mesa.save(update_fields=["status"])
        return pedido

    @staticmethod
    @transaction.atomic
    def adicionar_demanda(pedido_id, item_id, quantidade):
        pedido = Pedido.objects.get(pk=pedido_id)
        if pedido.status != Pedido.STATUS_ABERTO:
            raise ValueError(
                "Só é permitido adicionar demanda em pedido aberto.")

        item = Item.objects.get(pk=item_id)
        if not item.disponivel:
            raise ValueError(
                "Este item está indisponível para novas demandas.")

        if quantidade <= 0:
            raise ValueError("A quantidade deve ser positiva.")

        demanda = Demanda.objects.create(
            pedido=pedido,
            item=item,
            nome_item_snapshot=item.nome_item,
            quantidade=quantidade,
            preco_unitario=item.preco,
            status=Demanda.STATUS_PENDENTE,
        )
        pedido = Pedido.objects.get(pk=pedido_id)
        PedidoService.recalcular_total(pedido)
        return demanda

    @staticmethod
    @transaction.atomic
    def avancar_demanda(demanda_id):
        demanda = Demanda.objects.get(pk=demanda_id)
        if demanda.status == Demanda.STATUS_PENDENTE:
            demanda.status = Demanda.STATUS_EM_PREPARO
        elif demanda.status == Demanda.STATUS_EM_PREPARO:
            demanda.status = Demanda.STATUS_FINALIZADA
        else:
            raise ValueError("Esta demanda não pode avançar mais.")
        demanda.save(update_fields=["status"])
        pedido = demanda.pedido
        PedidoService.recalcular_total(pedido)
        return demanda

    @staticmethod
    @transaction.atomic
    def cancelar_demanda(demanda_id):
        demanda = Demanda.objects.get(pk=demanda_id)
        if demanda.status != Demanda.STATUS_PENDENTE:
            raise ValueError("Só é possível cancelar uma demanda pendente.")
        demanda.status = Demanda.STATUS_CANCELADA
        demanda.subtotal = Decimal("0.00")
        demanda.save(update_fields=["status", "subtotal"])
        PedidoService.recalcular_total(demanda.pedido)
        return demanda

    @staticmethod
    @transaction.atomic
    def cancelar_pedido(pedido_id):
        pedido = Pedido.objects.get(pk=pedido_id)
        if pedido.status != Pedido.STATUS_ABERTO:
            raise ValueError("Só é possível cancelar um pedido aberto.")

        if pedido.demandas.exclude(status=Demanda.STATUS_PENDENTE).exists():
            raise ValueError(
                "Pedido com demanda não pendente não pode ser cancelado.")

        for demanda in pedido.demandas.all():
            demanda.status = Demanda.STATUS_CANCELADA
            demanda.subtotal = Decimal("0.00")
            demanda.save(update_fields=["status", "subtotal"])

        pedido.status = Pedido.STATUS_CANCELADO
        pedido.valor_total = Decimal("0.00")
        pedido.save(update_fields=["status", "valor_total"])

        pedido.mesa.status = Mesa.STATUS_LIVRE
        pedido.mesa.save(update_fields=["status"])
        return pedido

    @staticmethod
    @transaction.atomic
    def fechar_pedido(pedido_id):
        pedido = Pedido.objects.get(pk=pedido_id)
        if pedido.status != Pedido.STATUS_ABERTO:
            raise ValueError("Só é possível fechar um pedido aberto.")

        if pedido.demandas.count() == 0:
            raise ValueError("Pedido sem demandas não pode ser fechado.")

        if pedido.demandas.exclude(status__in=[Demanda.STATUS_FINALIZADA, Demanda.STATUS_CANCELADA]).exists():
            raise ValueError(
                "Pedido com demanda pendente ou em preparo não pode ser fechado.")

        pedido.status = Pedido.STATUS_FECHADO
        pedido.save(update_fields=["status"])

        pedido.mesa.status = Mesa.STATUS_LIVRE
        pedido.mesa.save(update_fields=["status"])
        return pedido
