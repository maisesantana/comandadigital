<!--
Relatório de impacto da sincronização
Versão: 1.0.0 -> 1.1.0 (nova configuração obrigatória do Django)
Princípios modificados: nenhum; princípios existentes preservados.
Seções adicionadas: Configuração do Django.
Seções removidas: nenhuma.
Pendências: confirmar a data original de ratificação.
Este relatório é temporário e deve ser removido antes do commit da emenda.
-->

# Constituição do Comanda Digital

## Princípios Fundamentais

### 1. Qualidade e consistência do código
O código Python DEVE seguir PEP 8 e as convenções do Django. Models DEVEM usar CamelCase;
funções e variáveis DEVEM usar snake_case. Views DEVEM permanecer enxutas, coordenar as
requisições e delegar regras de negócio aos models. Templates DEVEM limitar-se à apresentação
e NÃO DEVEM conter regras de negócio. Toda mudança no esquema do banco de dados DEVE ser
registrada em uma migration versionada. Essas regras tornam o código previsível e mantêm
decisões de domínio fora da camada de apresentação.

### 2. Regras de domínio como invariantes
Uma mesa DEVE ter no máximo um pedido em aberto por vez. O total do pedido DEVE ser
recalculado automaticamente e NÃO DEVE ser editável manualmente. Um pedido NÃO DEVE ser
fechado enquanto houver demanda que não esteja finalizada ou cancelada; ao fechar o pedido,
a mesa DEVE ser liberada automaticamente. Cada regra DEVE ter uma única implementação
canônica, sem duplicação entre Pedido e Demanda. As operações de domínio DEVEM preservar essas
invariantes em todos os fluxos que alterem pedidos, demandas ou mesas.

### 3. Responsabilidades explícitas
O projeto DEVE seguir o padrão MVT do Django e separar os domínios em apps de cardápio,
mesas, pedidos e funcionarios. Relacionamentos entre models DEVEM ser declarados explicitamente
com ForeignKey e related_name. Pedido DEVE ser responsável pelo ciclo de vida e pelo total do
pedido; Demanda DEVE ser responsável pelo seu próprio estado de execução. Essa divisão define
uma fonte canônica para cada comportamento e evita regras concorrentes.

### 4. Funcionalidade acompanhada de interface
Cada funcionalidade DEVE ser desenvolvida junto com sua própria tela. A interface DEVE
organizar as áreas principais em abas: Cardápio, Mesas, Pedidos e Cozinha. Uma funcionalidade
demonstrada DEVE estar acessível pela interface correspondente, de modo que o comportamento
possa ser operado e verificado no fluxo de trabalho do restaurante.

### 5. Verificação manual documentada
Toda funcionalidade demonstrada DEVE ter ao menos um teste manual documentado com cenário e
resultado esperado. O projeto NÃO DEVE criar nem exigir testes automatizados. A documentação
manual DEVE permitir que outra pessoa repita o cenário e compare o resultado observado com o
resultado esperado.

## Arquitetura e regras de domínio

O padrão MVT do Django DEVE orientar a separação entre models, views e templates. Os apps
cardápio, mesas, pedidos e funcionarios DEVEM manter responsabilidades alinhadas aos respectivos
domínios. As regras invariantes deste documento prevalecem sobre decisões locais de
implementação. Toda alteração de esquema DEVE incluir sua migration correspondente; nenhuma
mudança de esquema pode depender de edição manual não versionada do banco de dados.

### Configuração do Django

O arquivo `settings.py` do projeto DEVE definir os seguintes valores:

```python
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = False
```

## Experiência e fluxo de desenvolvimento

As telas DEVEM acompanhar a entrega de cada funcionalidade e integrar-se às abas Cardápio,
Mesas, Pedidos e Cozinha. Antes de considerar uma funcionalidade demonstrada, a equipe DEVE
registrar seu cenário de teste manual e o resultado esperado. Revisões DEVEM verificar a
conformidade com estes princípios, inclusive as invariantes de pedidos, demandas e mesas, a
migration de alterações de esquema e a documentação do teste manual. Todo o conteúdo do projeto
e toda saída produzida pelo Spec Kit DEVE estar em Português do Brasil, exceto nomes de
tecnologias, ferramentas e comandos, que permanecem sem tradução.

## Governança

Esta constituição prevalece sobre convenções locais conflitantes. Alterações DEVEM ser propostas
neste documento, avaliadas quanto ao impacto sobre princípios, regras de domínio e trabalho
existente, e registradas com justificativa e data. Uma alteração não pode enfraquecer
silenciosamente uma invariante. A equipe DEVE revisar a conformidade durante a revisão de cada
funcionalidade demonstrada.

A versão DEVE seguir versionamento semântico MAJOR.MINOR.PATCH: MAJOR para remoção ou mudança
incompatível de princípios; MINOR para novos princípios, seções ou expansão material das
obrigações; PATCH para esclarecimentos e correções sem mudança de significado. Cada emenda
DEVE atualizar a data da última alteração e explicar o impacto da versão.

**Versão**: 1.1.0 | **Ratificada**: TODO(RATIFICATION_DATE): confirmar a data original de adoção | **Última alteração**: 2026-09-26
