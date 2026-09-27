# Plano de implementação: Comanda digital de restaurante

**Branch**: `001-comanda-digital` | **Data**: 2026-09-27 | **Especificação**: [spec.md](spec.md)

**Entrada**: [spec.md](spec.md) e requisitos de stack/arquitetura fornecidos para Django, SQLite e Bootstrap 5.

## Resumo

Aplicação web para gerenciar cardápio, mesas, pedidos e fila da cozinha em um único restaurante. Será iniciada como projeto Django com apps por domínio, templates compartilhados e SQLite. As regras de ciclo de vida e total ficam centralizadas em `Pedido`; `Demanda` controla somente o próprio estado de execução. A interface será entregue com cada fluxo e validada manualmente, sem testes automatizados.

## Contexto técnico

**Linguagem/versão**: Python 3.14.6, versão detectada no ambiente virtual existente.

**Dependências principais**: Django 6.1.1, versão instalada no ambiente virtual; Bootstrap 5 carregado por CDN, sem baixar recursos para o projeto.

**Armazenamento**: SQLite para desenvolvimento e demonstração local.

**Verificação**: Cenários manuais documentados em português, conforme a constituição. Não criar nem exigir testes automatizados. Comandos de verificação estrutural do Django e migrações continuam permitidos.

**Plataforma-alvo**: Navegador web atual, com execução local pelo servidor de desenvolvimento do Django.

**Tipo de projeto**: Aplicação web Django renderizada no servidor.

**Metas de desempenho**: Uso demonstrativo por uma operação de restaurante; não há meta de concorrência ou latência especificada.

**Restrições**: Sem autenticação, autorização ou modelos de funcionários; interface dividida nas áreas Cardápio, Mesas, Pedidos e Cozinha; CSS próprio simples com Bootstrap 5 via CDN. Configurar `LANGUAGE_CODE = 'pt-br'`, `TIME_ZONE = 'America/Sao_Paulo'`, `USE_I18N = True` e `USE_TZ = False`. Toda alteração de esquema requer migration versionada.

**Escopo**: CRUD de categorias e itens; conjunto fixo e predefinido de 10 mesas consultável pelo atendente; pedidos, demandas e fila da cozinha; cancelamento e fechamento com atualização automática da disponibilidade da mesa. Quando as 10 mesas estiverem ocupadas, novas aberturas ficam bloqueadas até uma liberação.

## Verificação da constituição

**Gate inicial: aprovado.**

- Qualidade: seguir PEP 8 e convenções Django; nomes de classes em CamelCase e atributos/funções em snake_case. Views coordenam e delegam regras aos models; templates ficam restritos à apresentação.
- Invariantes: no máximo um pedido aberto por mesa; total derivado das demandas não canceladas e sem edição manual; fechamento condicionado às demandas finalizadas/canceladas; liberação da mesa ao encerrar o pedido.
- Responsabilidades: MVT e apps `cardapio`, `mesas` e `pedidos`; `Pedido` é responsável pelo ciclo de vida e total, e `Demanda` pelo estado de execução.
- Interface: entregar telas junto com cada fluxo e navegação pelas áreas Cardápio, Mesas, Pedidos e Cozinha.
- Verificação: documentar cenários manuais repetíveis com resultados esperados; não criar nem exigir testes automatizados.
- Banco e configuração: migrations versionadas e valores de idioma/fuso horários conforme a constituição.

**Gate após o desenho: aprovado.** O modelo mantém `Pedido` como ponto canônico das transições de ciclo de vida e do total; alterações de demanda chamam essa lógica, sem duplicá-la em views. O status de mesa é atualizado na mesma operação de abrir, cancelar ou fechar pedido. Não há desvio da constituição.

## Estrutura do projeto

### Documentação desta funcionalidade

```text
specs/001-comanda-digital/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── interface.md
└── tasks.md                 # etapa posterior; não é criado pelo planejamento
```

### Código-fonte na raiz do repositório

```text
manage.py
requirements.txt
restaurante/
├── settings.py
├── urls.py
├── asgi.py
├── wsgi.py
├── cardapio/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
├── mesas/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── pedidos/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── cardapio/
│   ├── mesas/
│   ├── pedidos/
│   └── cozinha/
└── static/css/estilos.css
```

**Decisão de estrutura**: projeto Django e apps `cardapio`, `mesas` e `pedidos` sob `restaurante/`; `manage.py`, dependências e SQLite ficam na raiz. Templates centralizados e organizados por área. Não há app de funcionários, modelos de funcionários ou autenticação.

## Rastreamento de complexidade

Não há violações ou abstrações adicionais a justificar.

