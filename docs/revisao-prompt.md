# Revisão do prompt de origem

Revisão de `PROMPT_CRIACAO_SKILL_SAAS_BILLING_MF.md` feita em 2026-11-03, antes de criar a skill. O prompt original não foi alterado; as correções estão aplicadas nesta skill.

## Erros corrigidos no contrato

| # | Problema no prompt | Efeito se mantido | Correção |
|---|---|---|---|
| 1 | `assinaturas` (fase 03) tem FK para `provedores_pagamento` (fase 05) | A migration da fase 03 falharia | `provedores_pagamento` passou para a fase 03 |
| 2 | `assinaturas_itens` (fase 03) tem FK para `adicionais` (fase 06) | Idem | `assinaturas_itens` passou para a fase 06 |
| 3 | `provedores_pagamento.codigo` é UNIQUE sozinho | Impossível ter sandbox e produção do mesmo provedor | UNIQUE (`codigo`, `ambiente`) |
| 4 | Não havia estado antes da confirmação do pagamento | Assinatura paga sem estado válido até o webhook | Novo estado `pendente` |
| 5 | Tabelas filhas sem `tenant_id` | Isolamento dependia sempre de join | `tenant_id` em `assinaturas_itens`, `faturas_itens`, `assinaturas_historicos`, `assinaturas_alteracoes` e `pagamentos_reembolsos`; anulável em `pagamentos_eventos` |
| 6 | `planos_limites.periodicidade` anulável dentro de UNIQUE | Limites duplicados, pois NULL não colide | NOT NULL, com padrão `sem_periodo` |
| 7 | Plano "a partir de" ou por orçamento não cabia em `valor` | O exemplo Enterprise não tinha representação | Coluna `modalidade_preco`; `valor` anulável só em `sob_consulta` |
| 8 | Unicidade de `pagamentos_eventos` só "se o provedor garantir" | Sem deduplicação para os demais | `chave_deduplicacao` obrigatória; `evento_externo_id` anulável |
| 9 | Cupom exigia regras de cumulatividade, planos e ciclos sem colunas | Regra sem onde ser gravada | `cumulativo`, `planos_elegiveis`, `periodicidades_elegiveis` |
| 10 | Eventos de consumo imutáveis sem vínculo de compensação | Correção sem rastreabilidade | `evento_compensado_id` |

## Conflitos com as skills atuais

| # | Problema | Correção |
|---|---|---|
| 11 | Citava Laravel 12/PHP 8.4 e Vuetify 3 | Referência a `skill-backend-mf` e `skill-frontend-mf` 2.0.0: Laravel 13, PHP 8.5 (ou 8.4) e Vuetify 4 |
| 12 | A skill de backend pede autenticação de webhook além de segredo na URL, e chave por conta e ambiente | Incorporado às referências e à unicidade por linha de provedor |

## Lacunas de estrutura

| # | Problema | Correção |
|---|---|---|
| 13 | A trilha da seção 5 não tinha arquivo | `references/trilha-modulos.md` |
| 14 | Versão, checksum e mapeamento exigidos sem modelo | `templates/registro-aplicacao.yaml` e `templates/mapeamento-compatibilidade.yaml` |
| 15 | Validar YAML sem dependências, com Python padrão, não é possível em YAML livre | Manifesto em JSON, que também é YAML válido |
| 16 | Documentos manuais divergiriam do manifesto | `scripts/gerar_documentos.py` gera os derivados, e o validador confere |
| 17 | Laboratório sem definição | `tests/test_laboratorio_sqlite.py`, sem dependências; ver limites no relatório |
| 18 | Faltava o arquivo usado pelas outras skills MF | `agents/openai.yaml` |

## Decisões assumidas na revisão

São revisáveis, antes da primeira aplicação do contrato:

- Assinatura `pendente` conta como efetiva, para impedir duas contratações simultâneas.
- Mudança de plano altera a assinatura existente, via `assinaturas_alteracoes`, sem criar outra.
- Plano sem cobrança mantém `periodo_fim` e renova o período, para medir cotas.
- Todas as FKs usam RESTRICT, pois os dados são financeiros ou contratuais.
- Enumerações de fatura, pagamento, reembolso e histórico foram definidas aqui, já que o prompt pedia estados válidos sem listá-los.

## Mantido como estava

As 24 tabelas e seus nomes, os oito módulos, os gates, os preços de exemplo e a regra de não incluir requisitos de produto específico no núcleo.
