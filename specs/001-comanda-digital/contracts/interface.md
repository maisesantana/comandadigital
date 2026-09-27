# Contrato de interface: Comanda digital de restaurante

Este contrato descreve as telas HTML renderizadas pelo servidor para os papéis operacionais atendente e cozinha. Não existe API pública ou integração externa neste escopo. As áreas são acessíveis pela navegação comum, sem login ou controle de usuários.

## Navegação principal

A navegação persistente apresenta quatro destinos: **Cardápio**, **Mesas**, **Pedidos** e **Cozinha**. A tela atual deve permanecer identificável e os links devem funcionar sem depender de JavaScript.

| Área | Caminho base | Conteúdo e ações |
|---|---|---|
| Cardápio | `/cardapio/` | Listar categorias e itens; criar, editar e excluir categoria/item quando as relações permitirem; alterar disponibilidade do item. |
| Mesas | `/mesas/` | Listar as 10 mesas fixas e seu estado livre/ocupada; oferecer abertura de pedido somente para mesa livre. Atualizar o estado automaticamente quando pedido abrir, fechar ou for cancelado. |
| Pedidos | `/pedidos/` | Listar pedidos e estados; abrir detalhes de pedido; incluir demanda, ajustar quantidade pendente, cancelar demanda pendente, cancelar pedido elegível ou fechar pedido elegível. |
| Cozinha | `/cozinha/` | Listar demandas pendentes/em preparo com mesa, pedido, item, quantidade e estado; iniciar preparo ou finalizar demanda conforme transição permitida. |

## Contrato de ações

- Leitura de listas e detalhes é feita por requisição `GET`.
- Criação, edição, exclusão de itens/categorias, alteração de disponibilidade e transições de estado de pedido/demanda são feitas por formulários `POST`; não executar mutações via `GET`.
- Campos de preço total do pedido e subtotal da demanda são somente leitura e calculados pelo domínio.
- A ação de abrir pedido deve validar a situação atual da mesa no servidor; não confiar somente no estado exibido no navegador.
- A área Mesas não oferece criação, edição ou exclusão do conjunto fixo, nem alteração manual do estado da mesa.
- Se as 10 mesas estiverem ocupadas, não oferecer nem aceitar abertura de pedido até que uma mesa seja liberada.
- Ações de cancelamento e fechamento devem validar os estados atuais no servidor antes de gravar qualquer mudança.
- Após uma ação válida, apresentar confirmação e estado atualizado. Após ação inválida, explicar a regra violada, preservar os dados e manter o usuário na área pertinente.
- Formulários devem apresentar erros junto aos campos inválidos e conservar os dados fornecidos sempre que possível.
- As páginas usam templates Django, CSS simples do projeto e Bootstrap 5 por CDN. O conteúdo permanece utilizável por links e formulários HTML sem dependência de interação JavaScript para os fluxos principais.

## Estados observáveis

- A mesa exibe `livre` ou `ocupada`, estado atualizado automaticamente pelo ciclo do pedido, e oferece abrir pedido apenas quando estiver livre.
- O pedido exibe `aberto`, `fechado` ou `cancelado`, demandas, subtotais e total calculado.
- Cada demanda exibe `pendente`, `em preparo`, `finalizada` ou `cancelada`, além de item, quantidade e subtotal.
- A área Cozinha apresenta somente demandas pendentes ou em preparo; demandas canceladas e finalizadas não aparecem como trabalho ativo.
- Item indisponível continua visível no cardápio administrativo com seu estado, mas não pode ser incluído em nova demanda.

## Respostas para operações recusadas

- Mesa ocupada ou pedido aberto existente: recusar nova abertura e preservar o pedido existente.
- Item indisponível ou quantidade não positiva: recusar inclusão/alteração e indicar o campo ou a condição inválida.
- Cancelamento de demanda não pendente, cancelamento de pedido com demanda não pendente ou fechamento com demanda pendente/em preparo: recusar, informar a regra e manter pedido, demandas e mesa sem alterações parciais.
- Exclusão de categoria com itens associados ou de item usado por pedido aberto: preservar o registro e informar a referência impeditiva. Itens ligados somente a pedidos encerrados podem ser excluídos, preservando os snapshots nas demandas históricas.
- Quando as 10 mesas estiverem ocupadas: recusar qualquer nova abertura até que uma mesa seja liberada.
