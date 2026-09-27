# Especificação: Comanda digital de restaurante

**Funcionalidade**: `001-comanda-digital`

**Criada**: 2026-09-27

**Status**: Rascunho

**Entrada**: Descrição do usuário: centralizar o cardápio, as mesas e os pedidos de um restaurante, permitindo que atendentes conduzam pedidos e que a cozinha acompanhe o preparo das demandas.

## Cenários de uso e testes *(obrigatório)*

### História de usuário 1 - Manter cardápio e categorias (Prioridade: P1)

Como atendente, quero cadastrar e organizar categorias e itens do cardápio, editar seus dados e controlar a disponibilidade, para manter as opções oferecidas ao cliente atualizadas.

**Por que esta prioridade**: O cardápio é a base para registrar demandas e calcular valores corretos.

**Teste independente**: Cadastrar uma categoria e um item, alterar seus dados, marcar o item como indisponível e confirmar que ele não pode ser incluído em um novo pedido; depois, marcá-lo como disponível e confirmar que pode ser incluído.

**Cenários de aceitação**:

1. **Dado** que o atendente está na área Cardápio, **quando** cadastra uma categoria e um item com nome, preço e disponibilidade, **então** ambos aparecem associados e disponíveis para uso.
2. **Dado** que uma categoria ou item existe, **quando** o atendente edita seus dados ou o exclui, **então** a alteração aparece no cardápio e registros associados a pedidos existentes permanecem compreensíveis.
3. **Dado** que um item está indisponível, **quando** o atendente tenta adicioná-lo a uma nova demanda, **então** o sistema impede a inclusão; ao torná-lo disponível, a inclusão é permitida.

### História de usuário 2 - Abrir pedido e acompanhar valores (Prioridade: P1)

Como atendente, quero consultar a situação das mesas, abrir um pedido em uma mesa livre e adicionar itens com suas quantidades, para registrar o consumo e acompanhar subtotal e total sem cálculos manuais.

**Por que esta prioridade**: A abertura do pedido inicia o fluxo operacional e evita comandas duplicadas na mesma mesa.

**Teste independente**: Com duas mesas livres e uma ocupada, abrir um pedido em uma mesa livre, incluir itens em quantidades variadas e conferir os valores; tentar abrir outro pedido na mesa ocupada.

**Cenários de aceitação**:

1. **Dado** que uma mesa está livre, **quando** o atendente abre um pedido nela, **então** a mesa passa a ser identificada como ocupada e o pedido fica associado a ela.
2. **Dado** que uma mesa está ocupada por um pedido em aberto, **quando** o atendente tenta abrir outro pedido nessa mesa, **então** a operação é recusada e o pedido existente não é alterado.
3. **Dado** que um pedido está aberto e há um item disponível no cardápio, **quando** o atendente adiciona esse item com uma quantidade positiva, **então** a demanda exibe a quantidade e o subtotal correspondente, e o total do pedido é recalculado automaticamente.
4. **Dado** que o pedido tem uma demanda pendente, **quando** o atendente ajusta sua quantidade por uma ação permitida, **então** o subtotal e o total refletem a quantidade vigente, sem edição manual do total.

### História de usuário 3 - Preparar demandas na cozinha (Prioridade: P1)

Como integrante da cozinha, quero visualizar as demandas pendentes e em preparo e atualizar seu andamento, para preparar e finalizar os itens na ordem de trabalho.

**Por que esta prioridade**: O acompanhamento compartilhado do preparo reduz falhas de comunicação entre atendimento e cozinha.

**Teste independente**: Criar demandas em pedidos abertos, localizá-las na área Cozinha, iniciar o preparo e finalizar uma demanda, verificando o estado apresentado em cada etapa.

**Cenários de aceitação**:

1. **Dado** que existem demandas pendentes ou em preparo, **quando** a cozinha consulta sua área, **então** cada demanda aparece com seu pedido, mesa, item, quantidade e estado atual.
2. **Dado** que uma demanda está pendente, **quando** a cozinha inicia seu preparo, **então** seu estado passa para em preparo.
3. **Dado** que uma demanda está em preparo, **quando** a cozinha a finaliza, **então** seu estado passa para finalizada e deixa de ser apresentada como pendente de preparo.
4. **Dado** que uma demanda foi finalizada ou cancelada, **quando** alguém tenta retorná-la a um estado anterior, **então** a alteração é recusada.

### História de usuário 4 - Cancelar ou fechar pedido e liberar mesa (Prioridade: P1)

Como atendente, quero cancelar somente pedidos ainda não iniciados ou fechar pedidos concluídos, para manter a conta íntegra e disponibilizar a mesa ao próximo cliente.

**Por que esta prioridade**: O encerramento consistente protege a cobrança e completa o ciclo de uso da mesa.

**Teste independente**: Em pedidos distintos, tentar cancelar um pedido com demanda em preparo e outro cujas demandas estejam todas pendentes; tentar fechar um pedido com demanda ativa, depois finalizar ou cancelar as demandas restantes e fechar o pedido, verificando a situação da mesa.

**Cenários de aceitação**:

1. **Dado** que um pedido tem uma ou mais demandas não pendentes, **quando** o atendente tenta cancelar o pedido, **então** o cancelamento é recusado e o pedido permanece aberto.
2. **Dado** que todas as demandas do pedido estão pendentes, **quando** o atendente cancela o pedido, **então** o pedido é cancelado e a mesa é liberada.
3. **Dado** que uma demanda está pendente, **quando** o atendente a cancela, **então** ela passa para cancelada; se estiver em preparo ou finalizada, o cancelamento é recusado.
4. **Dado** que há ao menos uma demanda pendente ou em preparo, **quando** o atendente tenta fechar o pedido, **então** o fechamento é recusado.
5. **Dado** que todas as demandas estão finalizadas ou canceladas, **quando** o atendente fecha o pedido, **então** o pedido é encerrado e a mesa passa automaticamente a livre.

### Casos de borda

- Uma tentativa de abrir pedido em mesa ocupada deve ser recusada mesmo que a tela ainda mostre dados desatualizados da mesa.
- Quantidade zero ou negativa não pode ser registrada em uma demanda.
- Uma demanda cancelada não deve compor o valor cobrado no fechamento; uma demanda finalizada deve compor o total.
- Um pedido sem demandas pode ser cancelado, mas não pode ser fechado como conta concluída.
- Uma categoria que ainda contém itens não pode ser excluída até que esses itens sejam removidos ou associados a outra categoria.
- Um item usado em uma demanda de pedido aberto não pode ser excluído de forma que a demanda perca sua identificação ou seu valor.
- Tentativas de cancelar demanda ou pedido fora das condições permitidas devem informar que a operação não foi realizada e manter os estados anteriores.

## Requisitos *(obrigatório)*

### Requisitos funcionais

- **RF-001**: O sistema DEVE apresentar as áreas Cardápio, Mesas, Pedidos e Cozinha.
- **RF-002**: O atendente DEVE poder criar, consultar, editar e excluir categorias e itens do cardápio.
- **RF-003**: Cada item do cardápio DEVE pertencer a uma categoria e possuir nome, preço e estado de disponibilidade.
- **RF-004**: O atendente DEVE poder marcar um item como disponível ou indisponível; itens indisponíveis NÃO DEVEM ser adicionáveis a novas demandas.
- **RF-005**: O sistema DEVE apresentar as mesas com os estados livre ou ocupada, refletindo a existência de pedido em aberto.
- **RF-006**: O sistema DEVE permitir no máximo um pedido em aberto por mesa e DEVE recusar a abertura em mesa ocupada.
- **RF-007**: O atendente DEVE poder adicionar a um pedido demandas compostas por item do cardápio e quantidade inteira positiva.
- **RF-008**: Cada demanda DEVE apresentar seu item, quantidade, preço aplicável, subtotal e estado; o subtotal DEVE ser calculado pela quantidade multiplicada pelo preço aplicável.
- **RF-009**: O total do pedido DEVE ser recalculado a partir dos subtotais das demandas não canceladas e NÃO DEVE poder ser editado manualmente.
- **RF-010**: Cada demanda DEVE possuir um dos estados pendente, em preparo, finalizada ou cancelada.
- **RF-011**: A cozinha DEVE poder consultar as demandas pendentes e em preparo, com informação suficiente para identificar o pedido, a mesa, o item e a quantidade.
- **RF-012**: O estado de uma demanda DEVE avançar de pendente para em preparo e de em preparo para finalizada; uma demanda pendente também pode ser cancelada.
- **RF-013**: O sistema DEVE recusar o cancelamento de uma demanda cujo estado não seja pendente.
- **RF-014**: O sistema DEVE permitir cancelar um pedido somente quando todas as suas demandas estiverem pendentes; pedido sem demandas também pode ser cancelado.
- **RF-015**: O sistema DEVE recusar o fechamento do pedido enquanto houver demanda pendente ou em preparo e DEVE permitir o fechamento quando todas as demandas estiverem finalizadas ou canceladas.
- **RF-016**: Ao cancelar ou fechar um pedido, o sistema DEVE liberar automaticamente a mesa associada.
- **RF-017**: O atendente e a cozinha DEVEM conseguir identificar visualmente os estados de pedidos, demandas e mesas nas respectivas áreas.
- **RF-018**: O projeto DEVE documentar ao menos um teste manual reproduzível para cada funcionalidade demonstrada, incluindo cenário e resultado esperado; testes automatizados não fazem parte do escopo.

### Entidades principais

- **Categoria**: agrupamento de itens do cardápio; possui nome e itens associados.
- **Item do cardápio**: opção oferecida pelo restaurante; possui nome, preço, categoria e disponibilidade.
- **Mesa**: lugar de atendimento que pode estar livre ou ocupada por um único pedido em aberto.
- **Pedido**: conjunto de demandas associado a uma mesa, com estado de aberto, fechado ou cancelado e total calculado.
- **Demanda**: item e quantidade solicitados em um pedido, com preço aplicável, subtotal e estado de execução.
- **Atendente**: usuário responsável por manter o cardápio e conduzir pedidos e mesas.
- **Cozinha**: usuário responsável por consultar e atualizar o andamento de preparo das demandas.

## Critérios de sucesso *(obrigatório)*

### Resultados mensuráveis

- **CS-001**: Em todos os cenários manuais que tentem violar as regras de mesa, cancelamento ou fechamento, a operação proibida é recusada e nenhum estado relacionado é alterado indevidamente.
- **CS-002**: Em cinco pedidos de conferência, com diferentes itens e quantidades, subtotal e total correspondem aos preços aplicáveis e às demandas não canceladas, sem cálculo ou edição manual.
- **CS-003**: Um atendente consegue, em até dois minutos, selecionar uma mesa livre, abrir um pedido e adicionar três demandas com quantidades informadas, conferindo o total apresentado.
- **CS-004**: Em um roteiro manual completo, atendente e cozinha conseguem identificar a mesa, o item, a quantidade e o estado de cada demanda sem recorrer a uma comanda em papel para transmitir atualizações.

## Pressupostos

- O escopo cobre uma operação de restaurante e os papéis de atendente e cozinha; não inclui cadastro de funcionários, autenticação, pagamento ou emissão fiscal.
- Os usuários já têm acesso ao sistema e usam as áreas correspondentes ao seu papel; regras de login e permissões não foram especificadas.
- O preço aplicável à demanda é o preço do item no momento em que a demanda é adicionada; mudanças posteriores no cardápio não alteram pedidos já registrados.
- O atendente pode ajustar a quantidade somente enquanto a demanda estiver pendente; para retirar uma demanda do pedido, deve cancelá-la, preservando seu registro. Demandas em preparo ou finalizadas não podem ser editadas.
- A exclusão de categoria exige que ela não tenha itens associados. Um item ligado a demanda de pedido aberto não pode ser excluído enquanto essa demanda existir.
- O total não inclui taxas, descontos ou gorjetas, pois não foram solicitados.
- Cancelar um pedido com todas as demandas pendentes libera a mesa, assim como fechar um pedido com todas as demandas finalizadas ou canceladas.

## Verificação manual documentada

Os cenários de aceitação desta especificação são testes manuais: uma pessoa deve executar cada ação usando as áreas correspondentes e comparar o resultado observado com o resultado indicado. Para cobrir as invariantes centrais, repetir ao menos estes casos:

1. **Mesa ocupada**: abrir pedido em uma mesa livre e tentar abrir outro na mesma mesa. **Resultado esperado**: a segunda abertura é recusada e o pedido inicial permanece associado à mesa.
2. **Total automático**: adicionar duas demandas com preços e quantidades conhecidos; em seguida, cancelar uma demanda ainda pendente. **Resultado esperado**: subtotais e total são calculados sem edição manual e o total deixa de incluir a demanda cancelada.
3. **Cancelamento restrito**: tentar cancelar demanda em preparo e pedido com demanda em preparo; depois tentar cancelar uma demanda pendente. **Resultado esperado**: as duas primeiras operações são recusadas e somente a demanda pendente pode ser cancelada.
4. **Fechamento e liberação**: tentar fechar pedido com demanda pendente; finalizar ou cancelar todas as demandas e fechar novamente. **Resultado esperado**: a primeira tentativa é recusada; a segunda encerra o pedido e muda a mesa automaticamente para livre.
5. **Cardápio e cozinha**: tornar um item indisponível, tentar adicioná-lo ao pedido e acompanhar outra demanda desde pendente até finalizada na área Cozinha. **Resultado esperado**: o item indisponível não é adicionado e a demanda percorre os estados permitidos, com informações corretas de mesa, item e quantidade.
6. **Gerenciamento do cardápio**: criar uma categoria e um item, editar seus dados, excluí-los quando não houver vínculos impeditivos e tentar excluir uma categoria que ainda contenha item. **Resultado esperado**: criação, edição e exclusão permitidas aparecem na lista; a categoria com item associado não é excluída e o sistema informa a restrição.
