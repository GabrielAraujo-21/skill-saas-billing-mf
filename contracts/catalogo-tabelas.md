# Catálogo de tabelas

> Arquivo gerado por `scripts/gerar_documentos.py` a partir de `schema-manifest.yaml`. Não editar à mão.

Contrato `1.0.0`: 15 tabelas nucleares e 9 complementares.

| # | Tabela | Grupo | Natureza | Fase | Escopo | Timestamps | Exclusão |
|---|---|---|---|---|---|---|---|
| 1 | `planos` | Catálogo comercial | nuclear | 01 | global | completos | Soft delete; plano com versão publicada não é removido fisicamente. |
| 2 | `planos_versoes` | Catálogo comercial | nuclear | 01 | global | completos | Versão publicada é imutável quanto a direitos e preços; encerrar por status. |
| 3 | `planos_precos` | Catálogo comercial | nuclear | 01 | global | completos | Preço histórico nunca é sobrescrito; publicar nova versão. |
| 4 | `funcionalidades` | Catálogo comercial | nuclear | 02 | global | completos | Desativar por ativo; o código nunca é reaproveitado. |
| 5 | `planos_funcionalidades` | Catálogo comercial | nuclear | 02 | global | completos | Exclusão física bloqueada por FK RESTRICT; encerrar por status ou ativo. |
| 6 | `planos_limites` | Catálogo comercial | nuclear | 02 | global | completos | Exclusão física bloqueada por FK RESTRICT; encerrar por status ou ativo. |
| 7 | `assinaturas` | Contratação e utilização | nuclear | 03 | tenant | completos | Sem exclusão física; encerrar pela máquina de estados. |
| 8 | `assinaturas_itens` | Contratação e utilização | nuclear | 06 | tenant | completos | Desativar por ativo; preserva o snapshot. |
| 9 | `assinaturas_consumos` | Contratação e utilização | nuclear | 04 | tenant | completos | Agregado reconciliável com consumos_eventos; não excluir no período de retenção. |
| 10 | `provedores_pagamento` | Cobrança e pagamentos | nuclear | 03 | global | completos | Desativar por ativo. |
| 11 | `faturas` | Cobrança e pagamentos | nuclear | 05 | tenant | completos | Registro financeiro: sem soft delete nem exclusão; cancelar por status. |
| 12 | `pagamentos` | Cobrança e pagamentos | nuclear | 05 | tenant | completos | Registro financeiro: sem soft delete nem exclusão. |
| 13 | `adicionais` | Monetização complementar | nuclear | 06 | global | completos | Desativar por ativo; preço contratado fica no item da assinatura. |
| 14 | `cupons` | Monetização complementar | nuclear | 06 | global | completos | Desativar por ativo; preserva utilizações. |
| 15 | `cupons_utilizacoes` | Monetização complementar | nuclear | 06 | tenant | completos | Registro financeiro: sem exclusão; compensar por lançamento. |
| 16 | `faturas_itens` | Complementares padronizadas | complementar | 05 | tenant | completos | Registro financeiro: sem soft delete nem exclusão. |
| 17 | `assinaturas_historicos` | Complementares padronizadas | complementar | 03 | tenant | apenas_criacao | Trilha imutável: sem exclusão no período de retenção. |
| 18 | `assinaturas_alteracoes` | Complementares padronizadas | complementar | 03 | tenant | completos | Encerrar por status; preserva a trilha contratual. |
| 19 | `pagamentos_eventos` | Complementares padronizadas | complementar | 05 | tenant_opcional | completos | Sem exclusão antes da retenção definida; acesso restrito. |
| 20 | `pagamentos_reembolsos` | Complementares padronizadas | complementar | 05 | tenant | completos | Registro financeiro: sem soft delete nem exclusão. |
| 21 | `consumos_eventos` | Complementares padronizadas | complementar | 04 | tenant | apenas_criacao | Evento imutável: sem exclusão no período de retenção. |
| 22 | `tenants_beneficios` | Complementares padronizadas | complementar | 04 | tenant | completos | Encerrar por fim; preserva a auditoria. |
| 23 | `planos_adicionais` | Complementares padronizadas | complementar | 06 | global | completos | Exclusão física bloqueada por FK RESTRICT; encerrar por status ou ativo. |
| 24 | `planos_precos_provedores` | Complementares padronizadas | complementar | 05 | global | completos | Desativar por status. |

## Fases

| Fase | Módulo | Tabelas | Pré-condições | Gate |
|---|---|---|---|---|
| 00 | Diagnóstico e decisões | nenhuma | Ler projeto, skills, git status, governança e tenancy. | Inventário e ADRs aprovados. |
| 01 | Catálogo de planos | `planos`, `planos_versoes`, `planos_precos` | Fase 00; banco e padrão de IDs decididos. | Schema, CRUD administrativo, publicador versionado e testes. |
| 02 | Funcionalidades e limites | `funcionalidades`, `planos_funcionalidades`, `planos_limites` | Fase 01. | Entitlements e limites validados no backend. |
| 03 | Assinaturas | `assinaturas`, `provedores_pagamento`, `assinaturas_historicos`, `assinaturas_alteracoes` | Fases 01 e 02; tenants existentes. | Estados, ciclos, versionamento e isolamento. |
| 04 | Consumo | `assinaturas_consumos`, `consumos_eventos`, `tenants_beneficios` | Fase 03. | Concorrência, idempotência e reconciliação. |
| 05 | Financeiro e provedores | `faturas`, `pagamentos`, `faturas_itens`, `pagamentos_eventos`, `pagamentos_reembolsos`, `planos_precos_provedores` | Fases 01 e 03. | Testes em sandbox, webhooks e faturamento, sem cobrança real. |
| 06 | Adicionais e cupons | `assinaturas_itens`, `adicionais`, `cupons`, `cupons_utilizacoes`, `planos_adicionais` | Fases 03 a 05. | Regras de preço, limites e descontos com testes. |
| 07 | APIs, interface e métricas | nenhuma | Fases anteriores contratadas. | Contratos OpenAPI, filtros, RBAC, painel e E2E. |
