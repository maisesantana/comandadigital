# Especificação da Funcionalidade: Cardápio

**Ramo da Funcionalidade**: `[001-cardapio]`

**Criado**: 2026-09-25

**Status**: Rascunho

**Entrada**: Escopo da funcionalidade Cardápio: requisitos 1, 2, 3, 6 e 7.

## Objetivo

Definir o comportamento esperado para o cadastro e a organização do cardápio do restaurante, incluindo categorias e itens, sem inventar regras além do escopo definido.

## Cenários de Usuário e Testes *(obrigatório)*

### História de Usuário 1 - Cadastrar e organizar categorias (Priority: P1)

O restaurante precisa criar categorias para organizar os itens do cardápio e manter a estrutura funcional do menu.

**Por que esta prioridade**: A categoria é o agrupamento base para o cadastro de itens e determina a organização apresentada ao usuário.

**Teste Independente**: Um usuário informa o nome de uma categoria e confirma que a categoria é criada e listada corretamente.

**Cenários de Aceitação**:

1. **Dado** que o usuário informa um nome de categoria, **Quando** a categoria for criada, **Então** ela deve existir com o campo `nomeCategoria` preenchido.
2. **Dado** que a categoria foi criada, **Quando** a listagem for consultada, **Então** ela deve aparecer na relação de categorias.
3. **Dado** que uma categoria possui itens vinculados, **Quando** o usuário tentar excluí-la, **Então** a exclusão deve ser bloqueada e deve ser exibida uma mensagem de aviso.

---

### História de Usuário 2 - Cadastrar itens do cardápio (Priority: P1)

O restaurante precisa registrar itens do cardápio com dados básicos e associá-los a uma categoria existente.

**Por que esta prioridade**: Os itens são as unidades funcionais do cardápio e precisam estar corretamente vinculados para aparecerem no agrupamento correto.

**Teste Independente**: Um usuário cria um item com nome, preço, descrição opcional e categoria válida e confirma que ele aparece na categoria correta.

**Cenários de Aceitação**:

1. **Dado** que o usuário informa `nomeItem`, `preco`, `descricao` e uma categoria válida, **Quando** o item for criado, **Então** o item deve ser registrado e vinculado à categoria correta.
2. **Dado** que a descrição não foi informada, **Quando** o item for criado, **Então** a descrição pode permanecer opcional.
3. **Dado** que um item for criado sem categoria, **Quando** a operação for validada, **Então** o item deve ser rejeitado.

---

### História de Usuário 3 - Manter o cardápio atualizado (Priority: P2)

O restaurante precisa manter o cardápio consistente após alterações e remoções de itens e categorias.

**Por que esta prioridade**: Alterações e exclusões precisam refletir imediatamente na organização do cardápio para manter o ambiente consistente.

**Teste Independente**: Um item ou categoria é alterado ou removido e o resultado é validado imediatamente na listagem do cardápio.

**Cenários de Aceitação**:

1. **Dado** que um item existe, **Quando** ele for editado, **Então** a alteração deve ser refletida imediatamente.
2. **Dado** que um item existe, **Quando** ele for excluído, **Então** ele deve deixar de aparecer no agrupamento da categoria.
3. **Dado** que uma categoria está vazia, **Quando** ela for excluída, **Então** a exclusão deve ser permitida.

### Casos Limite

- O que acontece ao tentar excluir uma categoria que possui itens vinculados?
- O que acontece ao tentar criar um item sem categoria?
- O que acontece ao tentar criar uma categoria sem nome?

## Requisitos *(obrigatório)*

### Requisitos Funcionais

- **FR-001**: O sistema MUST permitir a criação de uma categoria informando o campo `nomeCategoria`.
- **FR-002**: O sistema MUST permitir listar categorias em uma relação de categorias.
- **FR-003**: O sistema MUST permitir a criação de um item com `nomeItem`, `preco`, `descricao` opcional e `categoria` obrigatória.
- **FR-004**: O sistema MUST garantir que todo item esteja vinculado a uma categoria existente.
- **FR-005**: O sistema MUST permitir editar itens e refletir alterações imediatamente.
- **FR-006**: O sistema MUST permitir excluir itens e refletir a exclusão imediatamente.
- **FR-007**: O sistema MUST agrupar itens por categoria no cardápio.
- **FR-008**: O sistema MUST impedir a exclusão de uma categoria que tenha itens vinculados.
- **FR-009**: O sistema MUST exibir uma mensagem de aviso quando a exclusão de categoria for bloqueada.
- **FR-010**: O sistema MUST permitir a exclusão de categorias sem itens vinculados.
- **FR-011**: O sistema MUST manter o cardápio como agregador das categorias cadastradas.
- **FR-012**: O sistema MUST manter a lista de categorias do cardápio sem inventar atributos adicionais.

### Entidades Principais *(incluir se a funcionalidade envolve dados)*

- **Categoria**: Entidade que representa um agrupamento de itens do cardápio, com nome definido pela propriedade `nomeCategoria`.
- **Item**: Entidade que representa um produto do cardápio, com nome, preço, descrição opcional e vínculo obrigatório a uma categoria.
- **Cardápio**: Agregador das categorias cadastradas, mantendo a organização da lista de categorias.

## Regras de Negócio

- A categoria é o agrupamento principal dos itens do cardápio.
- O item deve estar vinculado a uma categoria existente.
- A descrição do item é opcional.
- A exclusão de categoria com itens vinculados deve ser bloqueada.
- A categoria vazia pode ser removida.
- O cardápio organiza as categorias cadastradas e não define outros atributos além da lista de categorias.

## Dependências entre Funcionalidades

- A funcionalidade de Cardápio depende da existência de categorias para o correto agrupamento de itens.
- A funcionalidade de Pedidos depende dos itens do cardápio para compor as demandas.
- A funcionalidade de Interações de interface depende desta funcionalidade para exibir agrupamentos e preços corretamente.

## Critérios de Aceitação

- Uma categoria pode ser criada com `nomeCategoria` válido.
- Um item só pode existir com categoria válida.
- Os itens aparecem agrupados por categoria.
- A exclusão de categoria com itens vinculados é bloqueada com aviso.
- A exclusão de categoria sem itens vinculados é permitida.
- Alterações em itens e categorias são refletidas imediatamente.

## Premissas

- O escopo definido para esta funcionalidade inclui apenas as entidades e regras descritas neste documento.
- Não existem outros campos obrigatórios definidos para Categoria.
- No momento, o cardápio é tratado como agregador das categorias e não inclui atributos extras além da lista de categorias.
