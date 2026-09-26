# Especificação da Funcionalidade: Interfaces

**Ramo da Funcionalidade**: `[005-interfaces]`

**Criado**: 2026-09-25

**Status**: Rascunho

**Entrada**: Escopo da funcionalidade Interfaces atualizado para refletir o status booleano do pedido e os estados permitidos das demandas.

## Objetivo

Definir o comportamento esperado das telas principais do sistema, sem descrever detalhes técnicos de implementação além dos requisitos do escopo.

## Cenários de Usuário e Testes *(obrigatório)*

### História de Usuário 1 - Exibir o cardápio (Priority: P1)

O usuário precisa visualizar os itens do cardápio organizados por categoria e com dados essenciais exibidos corretamente.

**Por que esta prioridade**: O cardápio é a base da operação e precisa ser legível na tela.

**Teste Independente**: A tela de cardápio mostra os itens agrupados por categoria com nome, preço e descrição, mesmo quando a descrição não existe.

**Cenários de Aceitação**:

1. **Dado** que existem categorias e itens cadastrados, **Quando** a tela de cardápio for aberta, **Então** os itens devem aparecer agrupados por categoria.
2. **Dado** que um item possui descrição, **Quando** a tela for exibida, **Então** nome, preço e descrição devem aparecer.
3. **Dado** que um item não possui descrição, **Quando** a tela for exibida, **Então** a ausência de descrição não deve quebrar o layout.

---

### História de Usuário 2 - Exibir mesas e status (Priority: P1)

O usuário precisa ver todas as mesas e o status atual em uma visualização clara e consistente com o banco de dados.

**Por que esta prioridade**: O estado das mesas influencia diretamente o atendimento e a disponibilidade operacional.

**Teste Independente**: A tela de mesas lista todas as mesas com número e status, usando representação visual diferenciada e refletindo o status persistido.

**Cenários de Aceitação**:

1. **Dado** que existem mesas cadastradas, **Quando** a tela de mesas for aberta, **Então** todas devem ser listadas.
2. **Dado** que uma mesa possui status armazenado, **Quando** a tela for exibida, **Então** o número e o status devem corresponder ao status persistido.
3. **Dado** que existem diferentes estados de mesa, **Quando** a tela for renderizada, **Então** os status devem ser visualmente diferenciados.

---

### História de Usuário 3 - Exibir pedidos e demandas (Priority: P1)

O usuário precisa acompanhar o pedido aberto da mesa, suas demandas, itens e totais.

**Por que esta prioridade**: Esta interface concentra a operação principal do atendimento e precisa refletir o estado atual do pedido.

**Teste Independente**: A tela de pedidos mostra o pedido em aberto da mesa, as demandas e os itens com quantidade, subtotal e valor total, compatíveis com a soma dos subtotais.

**Cenários de Aceitação**:

1. **Dado** que uma mesa possui pedido com status `aberto`, **Quando** a tela de pedidos for aberta, **Então** o pedido em aberto deve ser exibido.
2. **Dado** que o pedido possui demandas, **Quando** a tela for carregada, **Então** as demandas devem aparecer junto aos itens associados.
3. **Dado** que cada item possui quantidade e subtotal, **Quando** o pedido for exibido, **Então** o valor total deve corresponder ao somatório dos subtotais.

---

### História de Usuário 4 - Exibir demandas da cozinha (Priority: P2)

A cozinha precisa visualizar as demandas com status `pendente` ou `em preparo` em ordem de espera.

**Por que esta prioridade**: A organização da fila de preparo é essencial para manter a ordem do atendimento e evitar retrabalho.

**Teste Independente**: A tela da cozinha mostra somente demandas com status `pendente` ou `em preparo`, ordenadas pela espera, sem exibir demandas `finalizada` ou `cancelada`.

**Cenários de Aceitação**:

1. **Dado** que existem demandas com status `pendente` ou `em preparo`, **Quando** a tela da cozinha for aberta, **Então** elas devem aparecer ordenadas pela espera, das mais antigas para as mais novas.
2. **Dado** que uma demanda está com status `finalizada` ou `cancelada`, **Quando** a tela da cozinha for exibida, **Então** ela não deve aparecer.
3. **Dado** que a tela da cozinha é consultada, **Quando** a listagem for montada, **Então** somente demandas em andamento devem ser exibidas.

### Casos Limite

- O que ocorre quando um item do cardápio não possui descrição?
- O que acontece quando o status da mesa está armazenado como `disponível` ou `ocupada`?
- O que acontece quando o pedido não possui demanda ativa?

## Requisitos *(obrigatório)*

### Requisitos Funcionais

- **FR-001**: O sistema MUST usar templates do Django para a tela de cardápio.
- **FR-002**: O sistema MUST exibir itens do cardápio agrupados por categoria.
- **FR-003**: O sistema MUST exibir nome, preço e descrição dos itens.
- **FR-004**: O sistema MUST garantir que a ausência de descrição não quebre o layout da tela de cardápio.
- **FR-005**: O sistema MUST exibir todas as mesas com número e status.
- **FR-006**: O sistema MUST utilizar representação visual diferenciada para os diferentes status das mesas.
- **FR-007**: O sistema MUST exibir o status correspondente ao valor armazenado no banco de dados.
- **FR-008**: O sistema MUST exibir o pedido com status `aberto` da mesa e suas demandas.
- **FR-009**: O sistema MUST exibir os itens dentro das demandas com quantidade e subtotal.
- **FR-010**: O sistema MUST exibir o `valorTotal` do pedido.
- **FR-011**: O sistema MUST garantir que o total exibido corresponda à soma dos subtotais.
- **FR-012**: O sistema MUST exibir demandas com status `pendente` ou `em preparo` na tela da cozinha.
- **FR-013**: O sistema MUST ordenar as demandas pela espera, mostrando primeiro as mais antigas.
- **FR-014**: O sistema MUST não exibir demandas com status `finalizada` ou `cancelada` na tela da cozinha.

### Entidades Principais *(incluir se a funcionalidade envolve dados)*

- **Tela de Cardápio**: Visualização dos itens agrupados por categoria.
- **Tela de Mesas**: Visualização da relação de mesas e status.
- **Tela de Pedidos**: Visualização do pedido ativo e suas demandas.
- **Tela da Cozinha**: Visualização da fila de demandas em andamento.

## Regras de Negócio

- O cardápio exibe itens por categoria e mantém a legibilidade da ausência de descrição.
- A tela de mesas deve refletir exatamente o status persistido.
- A tela de pedidos deve refletir o valor total calculado e os subtotais correspondentes.
- A tela da cozinha deve mostrar apenas demandas em andamento e na ordem de antiguidade.
- O status do pedido deve seguir a regra de `aberto` ou `fechado`.
- A demanda deve seguir somente os estados `pendente`, `em preparo`, `finalizada` e `cancelada`.

## Dependências entre Funcionalidades

- A tela de cardápio depende da funcionalidade de Cardápio.
- A tela de mesas depende da funcionalidade de Mesas.
- A tela de pedidos depende da funcionalidade de Pedidos.
- A tela da cozinha depende do status e da ordem das demandas da funcionalidade de Pedidos.

## Critérios de Aceitação

- A tela de cardápio exibe itens agrupados por categoria.
- A tela de mesas exibe todas as mesas com número e status corretos.
- A tela de pedidos exibe o pedido com status `aberto`, demandas, itens e total correto.
- A tela da cozinha exibe somente demandas em andamento, sem `finalizada` e `cancelada`, em ordem de antiguidade.
- A ausência de descrição não compromete o layout.

## Premissas

- Esta funcionalidade cobre apenas as telas definidas no escopo.
- A regra de apresentação de status foi definida pelos requisitos do sistema e deve ser respeitada.
- O pedido usa o status booleano `aberto` ou `fechado`.
- A demanda usa somente os estados `pendente`, `em preparo`, `finalizada` e `cancelada`.
