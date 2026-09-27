# Guia de validação manual: Comanda digital de restaurante

Este roteiro valida os fluxos pela interface do navegador. Ele não usa nem exige testes automatizados.

## Pré-requisitos

- Python 3.14.6 disponível e dependências listadas em `requirements.txt` instaladas no ambiente virtual.
- Acesso à internet para carregar o CSS do Bootstrap 5 pelo CDN.
- Ambiente local de demonstração; nenhum login é necessário.

## Preparar o ambiente

Na raiz do repositório, em PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations cardapio mesas pedidos
python manage.py migrate
```

Iniciar o servidor local:

```powershell
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/mesas/` no navegador. O ambiente deve apresentar as 10 mesas fixas do restaurante, além da navegação para Cardápio, Mesas, Pedidos e Cozinha.

## Cenários

### 1. Categorias, itens e disponibilidade

1. Na área Cardápio, criar uma categoria e dois itens com preços conhecidos.
2. Editar o nome e a descrição de um item; alterar sua disponibilidade para indisponível.
3. Tentar incluir esse item em um pedido e depois torná-lo disponível.
4. Excluir um item sem referências e tentar excluir uma categoria que ainda tenha item associado.

**Resultado esperado**: alterações válidas aparecem na listagem; item indisponível não entra em pedido; exclusões com referências impeditivas são recusadas sem perder dados.

### 2. Mesa ocupada e total automático

1. Na área Mesas, confirmar que as 10 mesas predefinidas aparecem na lista.
2. Abrir um pedido em uma mesa livre e confirmar que ela passa automaticamente a ocupada.
3. Tentar abrir outro pedido na mesma mesa.
4. No pedido inicial, adicionar dois itens disponíveis com quantidades positivas e conhecidas; conferir os subtotais e o total.
5. Ajustar a quantidade de uma demanda pendente e conferir o novo total; tentar informar quantidade zero.

**Resultado esperado**: o conjunto fixo aparece sem ações para alterá-lo; a segunda abertura e a quantidade inválida são recusadas; quantidades válidas recalculam subtotal/total automaticamente e nenhum campo permite editar manualmente o total.

### 3. Todas as mesas ocupadas

1. Abrir pedidos nas 10 mesas do conjunto predefinido.
2. Tentar abrir outro pedido quando todas estiverem ocupadas.
3. Cancelar um pedido vazio, conforme a regra de cancelamento, e confirmar que sua mesa fica livre.
4. Tentar abrir um pedido na mesa que foi liberada.

**Resultado esperado**: nenhuma nova abertura é aceita enquanto todas as mesas estão ocupadas; após a liberação automática de uma mesa, é possível abrir nela um novo pedido.

### 4. Fluxo da cozinha e cancelamentos

1. Na área Cozinha, localizar uma demanda pendente com pedido, mesa, item e quantidade visíveis.
2. Iniciar o preparo e confirmar o novo estado; tentar cancelar essa demanda pelo pedido.
3. Em outra demanda ainda pendente, cancelar a demanda.
4. Tentar cancelar o pedido que contém a demanda em preparo; depois cancelar um pedido cujas demandas estejam todas pendentes.

**Resultado esperado**: somente as transições permitidas são aceitas; cancelamento de demanda em preparo e de pedido com demanda não pendente é recusado; ao cancelar um pedido elegível, suas demandas pendentes passam a canceladas e a mesa fica livre.

### 5. Fechamento e liberação da mesa

1. Abrir pedido em uma mesa livre e adicionar duas demandas.
2. Tentar fechar enquanto ambas estão pendentes.
3. Iniciar preparo e finalizar uma demanda; cancelar a outra enquanto ainda pendente.
4. Fechar o pedido e consultar novamente a área Mesas.
5. Excluir do cardápio um item usado apenas pelo pedido já encerrado e reabrir os detalhes do pedido.

**Resultado esperado**: a primeira tentativa de fechamento é recusada; o pedido fecha somente quando todas as demandas estiverem finalizadas ou canceladas, e a mesa muda automaticamente para livre. O item pode ser excluído após o encerramento e a demanda histórica continua exibindo seu nome, quantidade e preço snapshot.

## Verificação estrutural opcional

Após a implementação, `python manage.py check` pode ser executado para verificar a configuração do projeto. Este comando não substitui os cenários manuais acima; nenhum comando de testes automatizados faz parte deste fluxo.
