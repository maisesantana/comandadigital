# Tasks: Comanda digital de restaurante

**Input**: Design documents from `/specs/001-comanda-digital/`

**Pré-requisitos**: `plan.md`, `spec.md`, `research.md`, `data-model.md` e `contracts/`.

**Testes**: A especificação exige validação manual documentada; não há testes automatizados no escopo.

**Organização**: as tarefas são agrupadas por história de usuário e por dependências de implementação.

## Formato: `[ID] [P?] [US?] Descrição com caminho do arquivo`

- **[P]**: tarefa paralelizável, em arquivos diferentes e sem dependência direta
- **[US1]**, **[US2]**, **[US3]**, **[US4]**: a história de usuário à qual a tarefa pertence
- Os caminhos devem refletir a estrutura definida no `plan.md`

## Phase 1: Setup (infraestrutura compartilhada)

**Objetivo**: preparar a base do projeto conforme a arquitetura aprovada.

- [X] T001 Criar a estrutura inicial do projeto Django em `restaurante/` com os apps `cardapio`, `mesas` e `pedidos`, além de `manage.py`, `requirements.txt` e `restaurante/settings.py`
- [X] T002 Configurar `restaurante/settings.py` com `LANGUAGE_CODE = 'pt-br'`, `TIME_ZONE = 'America/Sao_Paulo'`, `USE_I18N = True` e `USE_TZ = False`
- [X] T003 [P] Criar `restaurante/urls.py` e roteamento inicial das áreas Cardápio, Mesas, Pedidos e Cozinha
- [X] T004 [P] Definir `restaurante/templates/base.html` com a navegação principal e Bootstrap 5 por CDN
- [X] T005 [P] Criar diretórios de templates em `restaurante/templates/cardapio/`, `restaurante/templates/mesas/`, `restaurante/templates/pedidos/` e `restaurante/templates/cozinha/`
- [X] T006 [P] Criar `restaurante/static/css/estilos.css` para os estilos básicos da interface

---

## Phase 2: Fundamentos (pré-requisitos bloqueantes)

**Objetivo**: criar a base de domínio e a infraestrutura mínima que todas as histórias exigem.

**⚠️ CRÍTICO**: nenhuma história pode começar antes da conclusão desta fase.

- [X] T007 Definir `Categoria` e `Item` em `restaurante/cardapio/models.py` com nome, preço, categoria e disponibilidade
- [X] T008 Definir `Mesa` em `restaurante/mesas/models.py` com o conjunto fixo de 10 mesas e os estados livre e ocupada
- [X] T009 Definir `Pedido` e `Demanda` em `restaurante/pedidos/models.py` com status, total, quantidade, subtotal e snapshots de item/preço
- [X] T010 [P] Criar migrações iniciais e executar `python manage.py makemigrations` e `python manage.py migrate`
- [X] T011 [P] Implementar regras de domínio no serviço de pedidos em `restaurante/pedidos/services.py` para calculo de total, validação de estados e abertura/cancelamento/fechamento do pedido
- [X] T012 [P] Criar scaffolding inicial de views e formulários em `restaurante/cardapio/views.py`, `restaurante/cardapio/forms.py`, `restaurante/mesas/views.py`, `restaurante/pedidos/views.py` e `restaurante/pedidos/forms.py`

**Checkpoint**: a base do domínio está preparada para as histórias de usuário.

---

## Phase 3: User Story 1 - Manter cardápio e categorias (Prioridade: P1) 🎯 MVP

**Objetivo**: permitir que o atendente cadastre, edite e exclua categorias e itens, além de controlar a disponibilidade.

**Teste independente**: criar categoria e item, marcar um item como indisponível, tentar inseri-lo em novo pedido e, em seguida, torná-lo disponível novamente, confirmando que a regra de bloqueio opera corretamente.

### Implementação para User Story 1

- [ ] T013 [P] [US1] Implementar `Categoria` e `Item` em `restaurante/cardapio/models.py` com as regras de exclusão e associação previstas no plano
- [ ] T014 [P] [US1] Criar formulários em `restaurante/cardapio/forms.py` para categoria, item e alteração de disponibilidade
- [ ] T015 [US1] Implementar listagem, criação, edição e exclusão no `restaurante/cardapio/views.py`
- [ ] T016 [US1] Implementar templates de listagem e formulário em `restaurante/templates/cardapio/`
- [ ] T017 [US1] Registrar as rotas do cardápio em `restaurante/cardapio/urls.py` e integrar ao `restaurante/urls.py`
- [ ] T018 [US1] Validar manualmente a regra de que itens indisponíveis não entram em novas demandas e que categoria com itens associados não é excluída

**Checkpoint**: a área Cardápio está funcional e testável independentemente.

---

## Phase 4: User Story 2 - Gerenciar mesas, abrir pedido e acompanhar valores (Prioridade: P1)

**Objetivo**: consultar as mesas fixas, abrir pedidos em mesas livres e recalcular automaticamente os valores.

**Teste independente**: consultar as 10 mesas, abrir um pedido em mesa livre, adicionar demandas com quantidades válidas e verificar que o subtotal e o total são recalculados sem edição manual.

### Implementação para User Story 2

- [ ] T019 [P] [US2] Implementar `Mesa` em `restaurante/mesas/models.py` com o conjunto predefinido de 10 mesas e o status livre/ocupada
- [ ] T020 [P] [US2] Implementar `Pedido` e `Demanda` em `restaurante/pedidos/models.py` com `status`, `valor_total`, `quantidade`, `subtotal` e snapshots de item/preço
- [ ] T021 [US2] Implementar abertura de pedido, recusa em mesa ocupada e validação de quantidade positiva em `restaurante/pedidos/views.py` e `restaurante/pedidos/services.py`
- [ ] T022 [US2] Implementar adição de demanda, cálculo de subtotal e recálculo do total em `restaurante/pedidos/views.py` e `restaurante/pedidos/services.py`
- [ ] T023 [US2] Implementar listagem de mesas, detalhes de pedidos e fluxo de abertura em `restaurante/mesas/views.py` e `restaurante/templates/mesas/`
- [ ] T024 [US2] Implementar telas de pedido e demanda em `restaurante/pedidos/views.py` e `restaurante/templates/pedidos/`
- [ ] T025 [US2] Registrar as rotas de `mesas` e `pedidos` em `restaurante/mesas/urls.py` e `restaurante/pedidos/urls.py`
- [ ] T026 [US2] Validar manualmente o conjunto de 10 mesas, a recusa de abertura em mesa ocupada e o total automático do pedido

**Checkpoint**: a gestão de mesas e o ciclo de pedido estão funcionando de forma independente.

---

## Phase 5: User Story 3 - Preparar demandas na cozinha (Prioridade: P1)

**Objetivo**: permitir que a cozinha visualize demandas pendentes e em preparo e avance os estados conforme o preparo.

**Teste independente**: localizar uma demanda pendente, iniciar o preparo, finalizar a demanda e confirmar que a área da cozinha mostra corretamente o estado e as informações da mesa, item e quantidade.

### Implementação para User Story 3

- [ ] T027 [P] [US3] Implementar a listagem de demandas ativas e os filtros de cozinha em `restaurante/pedidos/views.py` e `restaurante/templates/cozinha/`
- [ ] T028 [US3] Implementar as transições de estado de demanda em `restaurante/pedidos/services.py` para `pendente -> em preparo -> finalizada`
- [ ] T029 [US3] Implementar a validação para impedir retorno de demandas finalizadas ou canceladas a estados anteriores
- [ ] T030 [US3] Construir a interface da cozinha em `restaurante/templates/cozinha/` com pedido, mesa, item, quantidade e estado
- [ ] T031 [US3] Registrar as rotas e ações do fluxo da cozinha em `restaurante/pedidos/urls.py` e `restaurante/urls.py`
- [ ] T032 [US3] Validar manualmente o fluxo da cozinha e a apresentação correta dos estados das demandas

**Checkpoint**: o fluxo de preparo e visualização da cozinha está funcional.

---

## Phase 6: User Story 4 - Cancelar ou fechar pedido e liberar mesa (Prioridade: P1)

**Objetivo**: encerrar pedidos somente quando permitido, liberar a mesa automaticamente e manter as invariantes do domínio.

**Teste independente**: tentar cancelar um pedido com demanda em preparo; cancelar um pedido elegível cujas demandas estejam todas pendentes; fechar um pedido quando todas as demandas estiverem finalizadas ou canceladas.

### Implementação para User Story 4

- [ ] T033 [P] [US4] Implementar as regras de cancelamento de demanda e pedido em `restaurante/pedidos/services.py`
- [ ] T034 [US4] Implementar o fechamento do pedido somente quando todas as demandas estiverem finalizadas ou canceladas em `restaurante/pedidos/services.py`
- [ ] T035 [US4] Atualizar automaticamente o estado da mesa para livre ao cancelar ou fechar um pedido em `restaurante/mesas/models.py` e `restaurante/pedidos/services.py`
- [ ] T036 [US4] Implementar os fluxos de ação em `restaurante/pedidos/views.py` e os feedbacks de erro/confirmação em `restaurante/templates/pedidos/`
- [ ] T037 [US4] Validar manualmente o cancelamento de demanda, o cancelamento e fechamento de pedido e a liberação da mesa associada
- [ ] T038 [US4] Validar manualmente o cenário em que as 10 mesas estão ocupadas e nenhuma nova abertura é aceita até a liberação de uma mesa

**Checkpoint**: o ciclo completo de pedido, demanda e mesa está coerente com as regras do sistema.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Objetivo**: revisar a qualidade final do entregável e garantir consistência com a constituição e o plano aprovado.

- [ ] T039 [P] Revisar `restaurante/cardapio/`, `restaurante/mesas/` e `restaurante/pedidos/` para confirmar nomes de modelos, `related_name` explícitos e invariantes do domínio
- [ ] T040 [P] Revisar `restaurante/templates/` e a navegação global para confirmar Cardápio, Mesas, Pedidos e Cozinha
- [ ] T041 [P] Executar `python manage.py check` e revisar migrações e estados de domínio sem criar testes automatizados
- [ ] T042 Validar manualmente os cenários principais para pedido, demanda, mesa e cozinha alinhados ao `spec.md` e ao `plan.md`

---

## Dependências e ordem de execução

### Dependências por fase

- **Fase 1**: sem dependência; pode começar imediatamente.
- **Fase 2**: depende da Fase 1; bloqueia todas as histórias.
- **Fases 3 a 6**: dependem da Fase 2; cada história pode ser entregue e validada independentemente.
- **Fase 7**: depende da conclusão das histórias e da validação manual.

### Ordem de histórias

1. **US1**: Cardápio e categorias (MVP)
2. **US2**: Mesas e pedidos
3. **US3**: Cozinha
4. **US4**: Cancelamento, fechamento e liberação de mesa

### Paralelização identificada

- T003, T004 e T005 podem ser executadas em paralelo.
- T010, T011 e T012 podem ser executadas em paralelo após a fase de setup.
- T013 e T014 podem ser executadas em paralelo dentro da US1.
- T019 e T020 podem ser executadas em paralelo dentro da US2.
- T027 e T028 podem ser executadas em paralelo dentro da US3.
- T033 e T034 podem ser executadas em paralelo dentro da US4.
- T039, T040 e T041 podem ser executadas em paralelo na fase final.

---

## Estratégia de implementação

### MVP primeiro (somente US1)

1. Concluir a Fase 1 e a Fase 2.
2. Implementar a US1.
3. Validar manualmente o cardápio.
4. Prosseguir para as histórias seguintes somente após a verificação.

### Entrega incremental

1. Cardápio funcional
2. Mesas e pedidos funcionais
3. Cozinha operacional
4. Cancelamento, fechamento e liberação de mesa
5. Revisão final e validação manual

---

## Observações

- As tarefas seguem o padrão obrigatório com `- [ ]`, IDs sequenciais e labels de história quando aplicáveis.
- Todos os caminhos refletem a estrutura aprovada em `plan.md` e não usam nomes de apps divergentes.
- A validação permanece manual, conforme a constituição e a especificação.
- Não há testes automatizados no escopo; o foco é a documentação e execução dos cenários manuais.
