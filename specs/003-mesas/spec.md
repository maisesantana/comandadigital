# Especificação da Funcionalidade: Mesas

**Ramo da Funcionalidade**: `[003-mesas]`

**Criado**: 2026-09-25

**Status**: Rascunho

**Entrada**: Escopo da funcionalidade Mesas: requisitos 5 e 8.

## Objetivo

Definir o comportamento esperado para o cadastro e a gestão de mesas do restaurante, respeitando as regras do escopo e sem incluir regras adicionais.

## Cenários de Usuário e Testes *(obrigatório)*

### História de Usuário 1 - Cadastrar e consultar mesas (Priority: P1)

O restaurante precisa registrar mesas e visualizar seu número e status para controlar os atendimentos.

**Por que esta prioridade**: A mesa é o ponto principal de atendimento e sua identificação e estado precisam ser consistentes para o funcionamento do sistema.

**Teste Independente**: Um usuário cria uma mesa e confirma que o número e o status aparecem corretamente na listagem.

**Cenários de Aceitação**:

1. **Dado** que uma mesa é criada com `numeroMesa` e `status`, **Quando** a mesa for registrada, **Então** ela deve existir com status inicial `disponível`.
2. **Dado** que a listagem de mesas for consultada, **Quando** as mesas forem exibidas, **Então** o número e o status devem aparecer corretamente.
3. **Dado** que o status da mesa for alterado manualmente, **Quando** a situação for excepcional, **Então** a alteração deve ser tratada somente em situações de manutenção.

---

### História de Usuário 2 - Controlar o status de forma automática (Priority: P1)

No fluxo normal, o status da mesa deve ser controlado automaticamente pelos pedidos e não por alteração manual.

**Por que esta prioridade**: Isso evita inconsistências entre a ocupação real da mesa e o status registrado no banco.

**Teste Independente**: O sistema mantém o status da mesa conforme o estado do pedido associado e a listagem reflete o valor armazenado.

**Cenários de Aceitação**:

1. **Dado** que uma mesa está sem pedido em andamento, **Quando** a situação for avaliada, **Então** o status deve refletir `disponível`.
2. **Dado** que uma mesa está associada a um pedido em curso, **Quando** o status for consultado, **Então** a listagem deve refletir o valor armazenado no banco.
3. **Dado** que o fluxo normal do pedido for aplicado, **Quando** o status for atualizado, **Então** a alteração deve ser automática e não manual.

### Casos Limite

- O que acontece se o status for alterado manualmente em uma situação excepcional?
- O que acontece quando a listagem de mesas é consultada e o status armazenado no banco diverge do que é esperado no fluxo?

## Requisitos *(obrigatório)*

### Requisitos Funcionais

- **FR-001**: O sistema MUST permitir o cadastro de uma mesa com o campo `numeroMesa`.
- **FR-002**: O sistema MUST permitir o cadastro de uma mesa com status informado, respeitando os valores permitidos `disponível` e `ocupada`.
- **FR-003**: O sistema MUST criar a mesa inicialmente com status `disponível`.
- **FR-004**: O sistema MUST listar todas as mesas.
- **FR-005**: O sistema MUST exibir o número e o status de cada mesa.
- **FR-006**: O sistema MUST tratar a alteração manual do status como exceção, não como fluxo normal.
- **FR-007**: O sistema MUST controlar automaticamente o status por meio dos pedidos no fluxo normal.
- **FR-008**: O sistema MUST manter a listagem de mesas refletindo o status armazenado no banco de dados.

### Entidades Principais *(incluir se a funcionalidade envolve dados)*

- **Mesa**: Entidade de atendimento com número identificador e status de disponibilidade.

## Regras de Negócio

- O status da mesa é restrito a `disponível` ou `ocupada`.
- A mesa é criada inicialmente em `disponível`.
- A alteração manual do status é excepcional e não deve ser o fluxo padrão.
- O status normal da mesa é controlado pelos pedidos.
- A listagem das mesas deve refletir o estado gravado no banco.

## Dependências entre Funcionalidades

- A funcionalidade de Mesas depende da existência de pedidos para controlar automaticamente o status no fluxo normal.
- A funcionalidade de Pedidos depende das mesas para associar cada pedido a uma única mesa.
- A funcionalidade de Interfaces depende desta funcionalidade para exibir a identificação e o status de cada mesa.

## Critérios de Aceitação

- A criação da mesa define `numeroMesa` e status inicial `disponível`.
- A listagem exibe número e status da mesa.
- O status permanecendo `disponível` ou `ocupada` é respeitado.
- O controle do status em fluxo normal é realizado por pedidos.
- A visualização da mesa reflete o status persistido no banco.

## Premissas

- Esta funcionalidade cobre somente o modelo e o gerenciamento das mesas definidos no escopo.
- Não existem outros status definidos além de `disponível` e `ocupada`.
- A alteração manual do status é permitida apenas em situações excepcionais e não deve substituir o fluxo de pedidos.
