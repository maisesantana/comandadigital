# Pesquisa e decisões: Comanda digital de restaurante

## Decisões

### Stack do projeto

- **Decisão**: usar Python 3.14.6 e Django 6.1.1, versões encontradas no ambiente virtual `venv` do workspace; usar SQLite e templates Django, conforme informado para a funcionalidade.
- **Justificativa**: acompanha o ambiente já preparado e as escolhas explícitas do projeto. SQLite atende ao uso local de desenvolvimento e demonstração, sem servidor de banco adicional.
- **Alternativas consideradas**: trocar a versão do Django por outra versão suportada ou adotar banco de dados de servidor. Não são necessárias para este escopo e divergem do ambiente e dos requisitos fornecidos.

### Organização Django

- **Decisão**: manter `manage.py` na raiz e colocar configuração, apps `cardapio`, `mesas` e `pedidos` e templates sob `restaurante/`; centralizar templates por área. Não criar app `funcionarios`.
- **Justificativa**: segue o layout apresentado pelo usuário e o padrão MVT obrigatório na constituição. A fila de cozinha usa views do domínio de pedidos e templates em `templates/cozinha/`, pois não foi solicitado um app de cozinha.
- **Alternativas consideradas**: separar frontend e backend, criar API externa ou espalhar templates pelos apps. Não agregam valor ao fluxo exclusivamente server-rendered solicitado.

### Papéis operacionais sem autenticação

- **Decisão**: tratar atendente e cozinha como papéis operacionais da interface, sem app `funcionarios`, models, autenticação, autorização ou gestão de usuários.
- **Justificativa**: o sistema não possui funcionalidade de autenticação, e os requisitos excluem explicitamente modelos de funcionários e controle de usuários. A constituição foi atualizada para remover a exigência anterior do app.
- **Alternativas consideradas**: criar um app ou modelos para representar funcionários, o que contraria o escopo informado.

### Gerenciamento de mesas

- **Decisão**: apresentar ao atendente um conjunto fixo e predefinido de 10 mesas, sem cadastro, edição ou exclusão durante a operação. O estado passa automaticamente a ocupada na abertura do pedido e a livre no fechamento ou cancelamento permitido.
- **Justificativa**: o número de mesas do sistema é fixo e o estado acompanha o ciclo de vida dos pedidos, conforme esclarecido pelo usuário. Quando todas as mesas estiverem ocupadas, não há mesa disponível para um novo pedido.
- **Quantidade definida**: 10 mesas fixas.

### Regras de domínio e consistência

- **Decisão**: `Pedido` é a fonte canônica para abrir, cancelar e fechar pedidos, recalcular o total e sincronizar o status da mesa. `Demanda` é a fonte canônica para suas próprias transições de estado. Executar cada transição e atualização relacionada em transação de banco.
- **Justificativa**: conserva as invariantes da constituição e evita duplicar lógica em views, forms ou templates. Uma restrição única condicional para pedidos abertos por mesa oferece proteção adicional no SQLite.
- **Alternativas consideradas**: calcular estados em views independentes ou permitir alteração direta dos status em formulários. Ambas tornam possível divergência entre pedido, demanda e mesa.

### Valores e histórico de demanda

- **Decisão**: representar valores com campos decimais; registrar na demanda o preço unitário e o nome do item como snapshots no momento da inclusão. Calcular o subtotal da demanda a partir da quantidade e do preço snapshot; recalcular `Pedido.valor_total` por uma única operação de domínio, excluindo demandas canceladas. Bloquear exclusão do item enquanto ligado a pedido aberto e, depois do encerramento, permitir a exclusão sem apagar os snapshots históricos.
- **Justificativa**: preserva valores e identificação históricos mesmo que o cardápio seja alterado depois. Impedir edição direta do total e atualizar seu valor após cada operação permitida mantém o campo solicitado e a invariável da constituição.
- **Alternativas consideradas**: usar ponto flutuante para moeda, que pode introduzir erros de arredondamento; usar apenas o preço atual do item, que alteraria o histórico; impedir a exclusão de qualquer item já vendido, o que restringiria permanentemente o CRUD; permitir edição do total, que viola a constituição.

### Cancelamento de pedido

- **Decisão**: ao cancelar um pedido cujas demandas estão todas pendentes, marcar essas demandas como canceladas na mesma transação, marcar o pedido como cancelado, recalcular seu total e liberar a mesa.
- **Justificativa**: evita que demandas de um pedido cancelado continuem aparecendo como trabalho pendente na cozinha e deixa pedido, demanda e mesa em estados coerentes.
- **Alternativas consideradas**: manter demandas pendentes após cancelar o pedido, o que deixa trabalho obsoleto na fila; cancelar apenas o pedido sem sincronizar as demandas, o que cria estados inconsistentes.

### Interface e Bootstrap

- **Decisão**: renderizar as páginas no servidor com templates Django, navegação comum pelas áreas Cardápio, Mesas, Pedidos e Cozinha, estilos próprios simples e Bootstrap 5 por CDN, fixando no template a versão escolhida e os metadados de integridade do recurso.
- **Justificativa**: cumpre o requisito visual e mantém os recursos do Bootstrap fora do repositório. A navegação deve continuar sendo links funcionais sem depender de JavaScript para as operações principais.
- **Alternativas consideradas**: baixar os arquivos do Bootstrap, contrariando o requisito; ou introduzir uma aplicação frontend/API separada, desnecessária para a experiência solicitada.

### Carga inicial de mesas

- **Decisão**: considerar o conjunto fixo de mesas previamente definido para o restaurante durante a validação manual; não adicionar fluxo de CRUD de mesas.
- **Justificativa**: a quantidade de mesas é predefinida e não muda durante a operação do sistema.

## Pressupostos e pontos para confirmar

- O sistema opera com exatamente 10 mesas predefinidas, que não são alteradas durante a operação.
- Não foram definidos requisitos de concorrência, publicação em servidor, navegadores mínimos, pagamentos ou disponibilidade sem internet. Permanecem fora deste planejamento de demonstração local.
- A versão menor exata do Bootstrap pode ser fixada durante a implementação ao selecionar o link CDN oficial disponível; o requisito informado fixa somente a linha major 5.

## Fontes consideradas

- Requisitos de stack, arquitetura e exclusão de autenticação fornecidos para esta funcionalidade.
- Especificação em `specs/001-comanda-digital/spec.md`.
- Constituição em `.specify/memory/constitution.md`.
- Ambiente local consultado: Python 3.14.6 e Django 6.1.1 no `venv`.
