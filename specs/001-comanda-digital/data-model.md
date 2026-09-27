# Modelo de dados: Comanda digital de restaurante

Os identificadores de atributos usam `snake_case`, conforme as convenções da constituição. Os nomes conceituais informados em português são mantidos nos modelos e na interface.

## Entidades

### Categoria (`cardapio`)

- `id`: chave primária.
- `nome_categoria`: texto obrigatório.
- Relacionamento: uma categoria pode possuir vários itens; cada item pertence a uma categoria.
- Exclusão: impedir excluir uma categoria enquanto houver itens associados.

### Item (`cardapio`)

- `id`: chave primária.
- `nome_item`: texto obrigatório.
- `preco`: decimal obrigatório, com duas casas decimais e valor não negativo.
- `descricao`: texto opcional.
- `categoria`: chave estrangeira obrigatória para Categoria, protegida contra exclusão enquanto houver item associado.
- `disponivel`: booleano, inicialmente verdadeiro.
- Exclusão: impedir excluir item referenciado por demanda de pedido aberto. Após o pedido deixar de estar aberto, permitir exclusão; as demandas históricas preservam nome e preço snapshots.

### Mesa (`mesas`)

- `id`: chave primária.
- `numero_mesa`: inteiro positivo, único.
- `status`: `livre` ou `ocupada`; inicialmente `livre`, atualizado automaticamente conforme abertura, fechamento ou cancelamento do pedido associado.
- Conjunto: existem exatamente 10 mesas, predefinidas para o restaurante; o atendente não cadastra, edita ou exclui mesas durante a operação.
- Relacionamento: uma mesa pode ter vários pedidos históricos, mas no máximo um pedido com status `aberto`.
- Consistência: Pedido atualiza o estado da mesa ao abrir, cancelar ou fechar pedido. O campo é mantido para apresentação direta na lista de mesas.
- Consulta: o atendente pode ver todas as mesas predefinidas e seus estados; não pode alterar diretamente o estado.

### Pedido (`pedidos`)

- `id`: chave primária.
- `mesa`: chave estrangeira obrigatória para Mesa; o conjunto fixo de mesas não é alterado durante a operação.
- `data_hora`: data e hora de abertura, preenchida automaticamente.
- `status`: `aberto`, `fechado` ou `cancelado`; começa como `aberto`.
- `valor_total`: decimal de duas casas, inicialmente zero, não editável por formulário; atualizado apenas pela operação canônica de recálculo do pedido.
- `observacao`: texto opcional.
- Relacionamento: um pedido possui várias demandas.
- Regra de unicidade: restrição condicional única para `mesa` quando `status = aberto`, além da validação de disponibilidade na abertura.
- Exclusão: não oferecer exclusão de pedido pela interface; encerramento é feito por cancelamento ou fechamento.

### Demanda (`pedidos`)

- `id`: chave primária.
- `pedido`: chave estrangeira obrigatória para Pedido.
- `item`: chave estrangeira opcional para Item, anulada quando um item histórico puder ser excluído.
- `nome_item_snapshot`: nome do item no momento em que a demanda foi criada.
- `quantidade`: inteiro positivo.
- `preco_unitario`: valor decimal copiado do item no momento em que a demanda foi criada; não é alterável manualmente.
- `data_hora`: data e hora de criação, preenchida automaticamente.
- `status`: `pendente`, `em preparo`, `finalizada` ou `cancelada`; começa como `pendente`.
- `subtotal`: valor calculado a partir da quantidade e do preço unitário snapshot; não é editável nem precisa ser armazenado como cópia independente.
- Relacionamento: uma demanda pertence a um pedido e referencia um item do cardápio.

Atendente e cozinha são papéis operacionais da interface, não entidades persistidas. Não criar modelos de funcionário, garçom, cozinheiro, administrador ou usuário para esta funcionalidade.

## Regras e transições

### Pedido e mesa

- Abrir pedido somente quando a mesa estiver `livre` e não existir pedido `aberto` para ela. Criar o pedido e marcar a mesa `ocupada` na mesma transação.
- Se as 10 mesas estiverem ocupadas, recusar abertura de pedido até que uma mesa volte a ficar livre.
- Criar uma restrição única condicional para impedir dois pedidos abertos associados à mesma mesa, mesmo quando uma validação prévia da tela estiver desatualizada.
- Cancelar pedido somente quando todas as demandas estiverem `pendente`. Na mesma transação, marcar essas demandas `cancelada`, marcar o pedido `cancelado`, recalcular o total e liberar a mesa. Pedido sem demandas também pode ser cancelado.
- Fechar pedido somente se houver ao menos uma demanda e todas estiverem `finalizada` ou `cancelada`. Na mesma transação, marcar o pedido `fechado` e a mesa `livre`.
- Pedido `fechado` e `cancelado` são estados terminais.

### Demanda e valores

- Criar demanda somente para pedido `aberto`, item disponível e quantidade positiva; copiar nome e preço do item para snapshots.
- Recusar exclusão do item enquanto houver demanda associada a pedido `aberto`; após o encerramento, permitir exclusão e manter a demanda histórica compreensível pelos snapshots.
- Permitir alterar quantidade somente enquanto a demanda estiver `pendente`; depois da alteração, recalcular o total do pedido.
- Permitir transições `pendente` para `em preparo`, `pendente` para `cancelada` e `em preparo` para `finalizada`. Estados `finalizada` e `cancelada` são terminais.
- Uma demanda cancelada não compõe o total. Demandas pendentes, em preparo e finalizadas compõem o total até eventual cancelamento permitido.
- Centralizar o recálculo em `Pedido`; operações de criação, alteração de quantidade e cancelamento de demanda chamam a operação do pedido, sem duplicar a fórmula em views ou templates.
- Executar mudanças de estado e atualização de valores/mesa em transação para não persistir estados parciais.

## Regras de integridade

- Todo valor monetário usa tipo decimal, nunca ponto flutuante binário.
- `valor_total` não aparece em formulários editáveis; a gravação ocorre somente pela operação de recálculo de Pedido.
- Campos de status usam escolhas fechadas definidas acima.
- Chaves estrangeiras e nomes de relacionamento devem ser explícitos, com `related_name` descritivo.
- Qualquer alteração do esquema deve gerar migration versionada.
- Configuração do projeto: `LANGUAGE_CODE = 'pt-br'`, `TIME_ZONE = 'America/Sao_Paulo'`, `USE_I18N = True` e `USE_TZ = False`.
