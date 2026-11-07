# Trilha de módulos

Cada fase tem ADR próprio ([modelo](../templates/adr-modulo.md)), testes e gate. Fase dependente não avança com gate reprovado. Fase não contratada fica adiada e registrada, sem criar tabelas vazias só para constar. As tabelas de cada fase estão no [catálogo](../contracts/catalogo-tabelas.md).

## Fase 00 — Diagnóstico e decisões

Sem tabelas. Ler projeto, skills, `git status`, governança e tenancy. Entregar a matriz de aderência e as decisões do [fluxo consultivo](fluxo-consultivo.md). **Gate:** inventário e ADRs aprovados.

## Fase 01 — Catálogo de planos

`planos`, `planos_versoes`, `planos_precos`. Depende do banco e do padrão de IDs. **Gate:** schema, CRUD administrativo, publicador que congela a versão e testes de imutabilidade.

## Fase 02 — Funcionalidades e limites

`funcionalidades`, `planos_funcionalidades`, `planos_limites`. **Gate:** resolvedor de direitos no backend e testes que provam que direito comercial não concede permissão de usuário.

## Fase 03 — Assinaturas

`assinaturas`, `provedores_pagamento`, `assinaturas_historicos`, `assinaturas_alteracoes`. `provedores_pagamento` entra aqui porque `assinaturas` tem FK para ela; nesta fase ela só contém dados de identificação. **Gate:** transições, ciclos, versionamento, uma assinatura efetiva por tenant e isolamento.

## Fase 04 — Consumo

`assinaturas_consumos`, `consumos_eventos`, `tenants_beneficios`. **Gate:** concorrência, idempotência e reconciliação entre eventos e agregados.

## Fase 05 — Financeiro e provedores

`faturas`, `pagamentos`, `faturas_itens`, `pagamentos_eventos`, `pagamentos_reembolsos`, `planos_precos_provedores`. Comece com um provedor, se o projeto decidir assim; o segundo reaproveita as mesmas tabelas. **Gate:** testes em sandbox, webhooks duplicados e fora de ordem, faturamento e nenhuma cobrança real.

## Fase 06 — Adicionais e cupons

`assinaturas_itens`, `adicionais`, `cupons`, `cupons_utilizacoes`, `planos_adicionais`. `assinaturas_itens` entra aqui porque tem FK para `adicionais`. **Gate:** regras de preço, limites e descontos testados, sem cupom duplicado.

## Fase 07 — APIs, interface e métricas

Sem tabelas novas. **Gate:** contratos OpenAPI, filtros, RBAC, painel e E2E. A [API pública](../contracts/api-publica-openapi.yaml) pode ser antecipada para depois da fase 02, se o projeto precisar exibir o catálogo antes.
