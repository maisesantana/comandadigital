# Especificação da Funcionalidade: Pedidos

**Ramo da Funcionalidade**: `[002-order-management]`

**Criado**: 2026-09-25

**Status**: Rascunho

**Entrada**: Escopo da funcionalidade Pedidos atualizado: o pedido usa status booleano representado por `aberto` ou `fechado`; as demandas usam os estados `pendente`, `em preparo`, `finalizada` e `cancelada`; e a demanda só pode ser cancelada quando estiver `pendente`.

## Objetivo

Definir o comportamento esperado do pedido do restaurante, incluindo sua associação à mesa, o controle do status do pedido, o ciclo de vida das demandas, a atualização do valor total e a consistência do atendimento, sem incluir regras fora do escopo informado.

## Cenários de Usuário e Testes *(obrigatório)*

### História de Usuário 1 - Criar pedido para mesa disponível (Priority: P1)

O restaurante precisa registrar pedidos somente em mesas disponíveis para manter a operação consistente.

**Por que esta prioridade**: A regra de associação entre pedido e mesa é base para o controle do atendimento.

**Teste Independente**: Um funcionário cria um pedido em uma mesa disponível e tenta criar outro pedido para a mesma mesa enquanto o primeiro permanece aberto.

**Cenários de Aceitação**:

1. **Dado** que uma mesa está disponível, **Quando** um pedido for criado, **Então** o pedido deve ser associado a essa mesa com status `aberto`.
2. **Dado** que a mesma mesa já possui um pedido com status `aberto`, **Quando** um novo pedido for tentado, **Então** a criação deve ser bloqueada.

---

### História de Usuário 2 - Adicionar demandas em pedidos abertos (Priority: P1)

O sistema precisa permitir que o pedido receba novas demandas enquanto estiver aberto e bloquear esse comportamento quando o pedido estiver fechado.

**Por que esta prioridade**: As demandas representam o que foi solicitado e devem poder ser incluídas enquanto o pedido permanece ativo.

**Teste Independente**: Um pedido com status `aberto` recebe novas demandas e um pedido com status `fechado` rejeita essa operação.

**Cenários de Aceitação**:

1. **Dado** que um pedido está com status `aberto`, **Quando** uma demanda for adicionada, **Então** a operação deve ser permitida.
2. **Dado** que um pedido está com status `fechado`, **Quando** uma nova demanda for tentada, **Então** a operação deve ser rejeitada.

---

### História de Usuário 3 - Atualizar o valor total automaticamente (Priority: P1)

O pedido deve manter o valor final atualizado como resultado das mudanças nas demandas ou nos itens do pedido.

**Por que esta prioridade**: O valor do pedido precisa refletir o estado correto do atendimento e evitar inconsistências na cobrança.

**Teste Independente**: O pedido é alterado e o valor total passa a refletir o novo estado sem intervenção manual.

**Cenários de Aceitação**:

1. **Dado** que o pedido possui demandas ou itens, **Quando** qualquer alteração for realizada, **Então** o valor total deve ser recalculado automaticamente.
2. **Dado** que o pedido recebe uma alteração válida, **Quando** o valor total for consultado, **Então** ele deve refletir o estado atual do pedido.

---

### História de Usuário 4 - Gerenciar status das demandas (Priority: P1)

Os estados de demanda devem seguir a padronização definida e a cancelamento deve ser permitido somente quando a demanda estiver pendente.

**Por que esta prioridade**: Esse padrão define a consistência da fila de produção e evita cancelamentos em estágios avançados do atendimento.

**Teste Independente**: A demanda pode mudar para `em preparo`, `finalizada` ou `cancelada` conforme as regras de negócio, e o cancelamento só é permitido quando a demanda estiver `pendente`.

**Cenários de Aceitação**:

1. **Dado** que uma demanda está com status `pendente`, **Quando** o cancelamento for solicitado, **Então** a operação deve ser permitida.
2. **Dado** que uma demanda está com status `em preparo`, **Quando** o cancelamento for solicitado, **Então** a operação deve ser bloqueada.
3. **Dado** que uma demanda está com status `finalizada`, **Quando** o cancelamento for solicitado, **Então** a operação deve ser bloqueada.
4. **Dado** que uma demanda está com status `cancelada`, **Quando** qualquer nova alteração for tentada, **Então** a operação deve ser bloqueada.

---

### História de Usuário 5 - Fechar pedido somente quando todas as demandas estiverem concluídas (Priority: P1)

O pedido só deve poder ser fechado quando todas as demandas estiverem concluídas ou canceladas de acordo com a regra do fluxo.

**Por que esta prioridade**: Isso garante que o atendimento não seja encerrado antes de todas as demandas estarem em estado compatível com o fechamento.

**Teste Independente**: O usuário tenta fechar um pedido que ainda tem demandas `pendente` ou `em preparo` e depois tenta novamente após todas as demandas estarem `finalizada` ou `cancelada`.

**Cenários de Aceitação**:

1. **Dado** que o pedido ainda possui demandas com status `pendente` ou `em preparo`, **Quando** a operação de fechamento for tentada, **Então** a operação deve ser bloqueada.
2. **Dado** que todas as demandas do pedido estão com status `finalizada` ou `cancelada`, **Quando** o pedido for fechado, **Então** o fechamento deve ser permitido.

---

### História de Usuário 6 - Liberar a mesa ao fechar o pedido (Priority: P2)

Quando o pedido é fechado, a mesa deve voltar a ficar disponível.

**Por que esta prioridade**: A liberação da mesa mantém a operação do restaurante consistente e permite que a mesa seja reutilizada.

**Teste Independente**: Um pedido com status `fechado` faz a mesa voltar para o estado disponível.

**Cenários de Aceitação**:

1. **Dado** que o pedido foi fechado, **Quando** o status da mesa for consultado, **Então** a mesa deve voltar a ficar disponível.
2. **Dado** que uma mesa está disponível, **Quando** um novo pedido for aberto, **Então** ela pode receber o novo atendimento sem conflitos.

### Casos Limite

- O que acontece ao tentar abrir um segundo pedido para a mesma mesa enquanto a primeira está aberta?
- O que acontece ao tentar adicionar demanda a um pedido com status `fechado`?
- O que acontece ao tentar cancelar uma demanda com status `em preparo`?
- O que acontece ao tentar fechar um pedido que ainda tem demandas `pendente` ou `em preparo`?

## Requisitos *(obrigatório)*

### Requisitos Funcionais

- **FR-001**: O sistema MUST associar cada pedido a uma única mesa.
- **FR-002**: O sistema MUST registrar, para cada pedido, a data e a hora do registro.
- **FR-003**: O sistema MUST registrar, para cada pedido, o status booleano do pedido, com semântica de `aberto` ou `fechado`.
- **FR-004**: O sistema MUST registrar, para cada pedido, o valor total.
- **FR-005**: O sistema MUST impedir que uma mesa tenha mais de um pedido com status `aberto` ao mesmo tempo.
- **FR-006**: O sistema MUST permitir que novos pedidos sejam criados apenas para mesas disponíveis.
- **FR-007**: O sistema MUST permitir que um pedido receba novas demandas enquanto estiver com status `aberto`.
- **FR-008**: O sistema MUST bloquear a inclusão de novas demandas quando o pedido estiver com status `fechado`.
- **FR-009**: O sistema MUST recalcular automaticamente o valor total do pedido quando houver alteração em demandas ou itens.
- **FR-010**: O sistema MUST definir os estados permitidos para demanda como `pendente`, `em preparo`, `finalizada` e `cancelada`.
- **FR-011**: O sistema MUST permitir que uma demanda seja cancelada somente quando estiver com status `pendente`.
- **FR-012**: O sistema MUST impedir o fechamento do pedido enquanto houver demandas com status `pendente` ou `em preparo`.
- **FR-013**: O sistema MUST permitir o fechamento do pedido somente quando todas as demandas estiverem com status `finalizada` ou `cancelada`.
- **FR-014**: O sistema MUST liberar a mesa quando o pedido for fechado.

### Entidades Principais *(incluir se a funcionalidade envolve dados)*

- **Mesa**: Local de atendimento com status de disponibilidade e associação a um pedido ativo.
- **Pedido**: Entidade principal do atendimento, com associação à mesa, data e hora, status booleano, valor total e demandas.
- **Demanda**: Solicitação contida no pedido com status definido entre `pendente`, `em preparo`, `finalizada` e `cancelada`.

## Regras de Negócio

- Cada pedido pertence a uma única mesa.
- A mesa disponível pode receber um novo pedido.
- A mesa ocupada não pode receber outro pedido com status `aberto`.
- O pedido pode receber novas demandas enquanto estiver com status `aberto`.
- O pedido não pode receber novas demandas quando estiver com status `fechado`.
- O valor total do pedido deve ser recalculado automaticamente após alterações nas demandas ou nos itens.
- A demanda aceita somente os estados `pendente`, `em preparo`, `finalizada` e `cancelada`.
- A demanda só pode ser cancelada quando estiver `pendente`.
- O pedido somente pode ser fechado quando todas as demandas estiverem `finalizada` ou `cancelada`.
- A mesa deve voltar a ficar disponível quando o pedido for fechado.

## Dependências entre Funcionalidades

- A funcionalidade de Pedidos depende da funcionalidade de Mesas para a disponibilidade da mesa.
- A funcionalidade de Pedidos depende da funcionalidade de Cardápio para a origem das demandas e dos itens do pedido.
- A funcionalidade de Interfaces depende da funcionalidade de Pedidos para exibir os pedidos, as demandas e o valor total.

## Critérios de Aceitação

- Um pedido é criado para uma mesa disponível e associado a ela com status booleano `aberto`.
- Uma mesa ocupada não recebe outro pedido com status `aberto`.
- Pedidos com status `aberto` aceitam novas demandas.
- Pedidos com status `fechado` não aceitam novas demandas.
- O valor total é recalculado sempre que o pedido é alterado.
- A demanda pode ser cancelada somente quando estiver `pendente`.
- O pedido só é fechado após todas as demandas estarem `finalizada` ou `cancelada`.
- A mesa volta a ficar disponível ao fechar o pedido.
- A demanda respeita apenas os estados `pendente`, `em preparo`, `finalizada` e `cancelada`.

## Premissas

- Esta funcionalidade cobre apenas o comportamento do pedido definido no escopo.
- Não há regras adicionais de cálculo, métricas, prazos ou fluxos inventados fora do escopo.
- O status do pedido é representado por uma regra booleana de `aberto` ou `fechado`.
- O status da demanda é limitado aos valores `pendente`, `em preparo`, `finalizada` e `cancelada`.
