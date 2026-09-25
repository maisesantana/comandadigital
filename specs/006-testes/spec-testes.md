# Especificação da Funcionalidade: Testes

**Ramo da Funcionalidade**: `[006-testes]`

**Criado**: 2026-09-25

**Status**: Rascunho

**Entrada**: Escopo da funcionalidade Testes atualizado para validar o novo padrão de status do pedido e das demandas.

## Objetivo

Definir os cenários de validação manual de regras e comportamento do sistema de comandas conforme o novo padrão de status do pedido e das demandas, sem incluir testes adicionais fora do escopo.

## Cenários de Usuário e Testes *(obrigatório)*

### História de Usuário 1 - Validar criação e bloqueio de pedido (Priority: P1)

A validação deve cobrir a criação de pedidos em mesas disponíveis e o bloqueio em mesas ocupadas.

**Por que esta prioridade**: A criação e o bloqueio de pedidos são regras fundamentais do atendimento e da consistência do sistema.

**Teste Independente**: O usuário executa manualmente os cenários de criação de pedido em mesa disponível e criação em mesa ocupada.

**Cenários de Aceitação**:

1. **Dado** que uma mesa está disponível, **Quando** um pedido for criado, **Então** a criação deve ser permitida e o pedido deve assumir status `aberto`.
2. **Dado** que uma mesa está ocupada com um pedido `aberto`, **Quando** um novo pedido for tentado, **Então** a criação deve ser bloqueada.

---

### História de Usuário 2 - Validar alteração de demandas no pedido (Priority: P1)

A validação deve cobrir a inclusão e a alteração de demandas em pedido aberto e o bloqueio em pedido fechado.

**Por que esta prioridade**: A capacidade de alterar ou adicionar demandas em pedido válido é parte central do fluxo operacional.

**Teste Independente**: O usuário testa a criação de demanda em pedido aberto e o bloqueio em pedido fechado.

**Cenários de Aceitação**:

1. **Dado** que um pedido está com status `aberto`, **Quando** uma demanda for adicionada, **Então** a ação deve ser permitida.
2. **Dado** que um pedido está com status `fechado`, **Quando** uma demanda for adicionada, **Então** a ação deve ser bloqueada.

---

### História de Usuário 3 - Validar regras de status das demandas e fechamento do pedido (Priority: P1)

A validação deve cobrir a alteração de itens e quantidades de demandas `pendente`, o bloqueio de alterações em demandas `em preparo` e o fechamento condicional do pedido.

**Por que esta prioridade**: Essas regras definem a integridade do pedido e do fluxo de produção.

**Teste Independente**: O usuário executa os cenários de alteração de demanda `pendente`, tentativa de alteração em `em preparo`, fechamento com demanda `pendente` ou `em preparo` e fechamento com todas as demandas `finalizada` ou `cancelada`.

**Cenários de Aceitação**:

1. **Dado** que uma demanda está com status `pendente`, **Quando** seus itens ou quantidades forem alterados, **Então** a alteração deve ser permitida.
2. **Dado** que uma demanda está com status `em preparo`, **Quando** seus itens ou quantidades forem modificados, **Então** a alteração deve ser rejeitada.
3. **Dado** que um pedido possui demanda com status `pendente` ou `em preparo`, **Quando** a operação de fechamento for tentada, **Então** o fechamento deve ser bloqueado.
4. **Dado** que todas as demandas do pedido estão com status `finalizada` ou `cancelada`, **Quando** o pedido for fechado, **Então** o fechamento deve ser permitido.

---

### História de Usuário 4 - Validar cancelamento de demanda (Priority: P1)

A validação deve confirmar que uma demanda só pode ser cancelada quando estiver pendente.

**Por que esta prioridade**: Esse comportamento evita cancelamentos indevidos em etapas avançadas do atendimento.

**Teste Independente**: O usuário tenta cancelar uma demanda pendente e tenta cancelar uma demanda em preparo ou finalizada.

**Cenários de Aceitação**:

1. **Dado** que uma demanda está com status `pendente`, **Quando** o cancelamento for solicitado, **Então** a operação deve ser permitida.
2. **Dado** que uma demanda está com status `em preparo`, **Quando** o cancelamento for solicitado, **Então** a operação deve ser bloqueada.
3. **Dado** que uma demanda está com status `finalizada`, **Quando** o cancelamento for solicitado, **Então** a operação deve ser bloqueado.

---

### História de Usuário 5 - Validar liberação da mesa (Priority: P2)

A validação deve confirmar que a mesa volta a ficar disponível quando o pedido é fechado.

**Por que esta prioridade**: A liberação da mesa permite que o atendimento continue em outra operação sem conflito de ocupação.

**Teste Independente**: O usuário fecha um pedido e valida que a mesa volta a assumir status disponível.

**Cenários de Aceitação**:

1. **Dado** que um pedido está aberto, **Quando** ele for fechado, **Então** o status do pedido deve mudar para `fechado`.
2. **Dado** que o pedido foi fechado, **Quando** a mesa for consultada, **Então** ela deve voltar para status disponível.

### Casos Limite

- O que acontece ao tentar alterar uma demanda em `em preparo`?
- O que acontece ao tentar cancelar uma demanda em `em preparo` ou `finalizada`?
- O que acontece ao tentar fechar um pedido com demanda `pendente`?

## Requisitos *(obrigatório)*

### Requisitos Funcionais

- **FR-001**: O sistema MUST ser testado manualmente para criação de pedido em mesa disponível.
- **FR-002**: O sistema MUST ser testado manualmente para tentativa de criação de pedido em mesa ocupada por pedido `aberto`.
- **FR-003**: O sistema MUST ser testado manualmente para adicionar demanda a pedido com status `aberto`.
- **FR-004**: O sistema MUST ser testado manualmente para tentativa de adicionar demanda a pedido com status `fechado`.
- **FR-005**: O sistema MUST ser testado manualmente para alteração de itens e quantidades de demanda com status `pendente`.
- **FR-006**: O sistema MUST ser testado manualmente para tentativa de alteração de itens e quantidades de demanda com status `em preparo`.
- **FR-007**: O sistema MUST ser testado manualmente para cancelamento de demanda somente quando a demanda estiver com status `pendente`.
- **FR-008**: O sistema MUST ser testado manualmente para tentativa de cancelamento de demanda com status `em preparo` ou `finalizada`.
- **FR-009**: O sistema MUST ser testado manualmente para tentativa de fechamento de pedido com demanda `pendente` ou `em preparo`.
- **FR-010**: O sistema MUST ser testado manualmente para fechamento do pedido quando todas as demandas estiverem `finalizada` ou `cancelada`.
- **FR-011**: O sistema MUST ser testado manualmente para liberação da mesa após o fechamento do pedido.

### Entidades Principais *(incluir se a funcionalidade envolve dados)*

- **Pedido**: Entidade de negócio cujo comportamento gera os cenários de teste.
- **Demanda**: Entidade cujos status e alterações são validados nos cenários.
- **Mesa**: Entidade cuja disponibilidade é validada no fluxo de criação e bloqueio de pedidos.

## Regras de Negócio

- Os cenários de teste devem validar apenas os comportamentos definidos no escopo.
- Os testes não devem cobrir regras fora do escopo informado.
- Os cenários de teste são manuais e devem validar as regras de negócio e o fluxo definido.
- O pedido usa apenas os status booleanos semânticos `aberto` e `fechado`.
- A demanda usa apenas os estados `pendente`, `em preparo`, `finalizada` e `cancelada`.
- A demanda só pode ser cancelada quando estiver `pendente`.

## Dependências entre Funcionalidades

- A funcionalidade de Testes depende dos comportamentos definidos em Cardápio, Mesas, Funcionários e Pedidos.
- A funcionalidade de Testes valida as regras de negócio das interfaces e da operação do sistema.

## Critérios de Aceitação

- Os cenários listados no escopo são executados manualmente e confirmam o comportamento esperado.
- Os bloqueios de criação, alteração, cancelamento e fechamento estão validados.
- A mesa fica disponível após o fechamento do pedido.
- Os estados de pedido e demanda seguem o padrão padronizado.

## Premissas

- Esta funcionalidade é válida apenas para os cenários e regras definidos no escopo.
- O pedido usa o status booleano semântico `aberto` e `fechado`.
- A demanda usa apenas os estados `pendente`, `em preparo`, `finalizada` e `cancelada`.
- O cancelamento da demanda só é permitido quando ela está em `pendente`.
