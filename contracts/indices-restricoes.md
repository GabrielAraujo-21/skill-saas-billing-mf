# Índices e restrições

> Arquivo gerado por `scripts/gerar_documentos.py` a partir de `schema-manifest.yaml`. Não editar à mão.

## `planos`

- UNIQUE `uq_planos_slug` (slug)

## `planos_versoes`

- UNIQUE `uq_planos_versoes_plano_numero` (plano_id, numero_versao)
- CHECK `trial_dias >= 0`
- CHECK `vigencia_fim IS NULL OR vigencia_inicio IS NULL OR vigencia_fim > vigencia_inicio`

## `planos_precos`

- UNIQUE `uq_planos_precos_versao_period_moeda` (plano_versao_id, periodicidade, moeda)
- CHECK `(modalidade_preco = 'sob_consulta' AND valor IS NULL) OR (modalidade_preco <> 'sob_consulta' AND valor IS NOT NULL AND valor >= 0)`
- CHECK `valor_implantacao >= 0`

## `funcionalidades`

- UNIQUE `uq_funcionalidades_codigo` (codigo)

## `planos_funcionalidades`

- UNIQUE `uq_planos_func_versao_func` (plano_versao_id, funcionalidade_id)
- INDEX `idx_planos_funcionalidades_funcionalidade_id` (funcionalidade_id)

## `planos_limites`

- UNIQUE `uq_planos_limites_versao_rec_period` (plano_versao_id, recurso, periodicidade)
- CHECK `limite IS NULL OR limite >= 0`

## `assinaturas`

- UNIQUE `uq_assinaturas_tenant_efetiva` (tenant_id) onde `status NOT IN ('cancelada', 'expirada')`
- UNIQUE `uq_assinaturas_provedor_externa` (provedor_pagamento_id, assinatura_externa_id)
- INDEX `idx_assinaturas_tenant_status` (tenant_id, status)
- INDEX `idx_assinaturas_status_cobranca` (status, proxima_cobranca_em)
- INDEX `idx_assinaturas_plano_versao_id` (plano_versao_id)
- INDEX `idx_assinaturas_plano_preco_id` (plano_preco_id)
- CHECK `valor_contratado >= 0`
- CHECK `periodo_fim > periodo_inicio`

## `assinaturas_itens`

- INDEX `idx_assinaturas_itens_tenant_assinatura` (tenant_id, assinatura_id)
- INDEX `idx_assinaturas_itens_assinatura_id` (assinatura_id)
- INDEX `idx_assinaturas_itens_adicional_id` (adicional_id)
- CHECK `quantidade > 0`
- CHECK `valor_unitario >= 0`
- CHECK `valor_total >= 0`

## `assinaturas_consumos`

- UNIQUE `uq_consumos_assinatura_rec_periodo` (assinatura_id, recurso, periodo_inicio, periodo_fim)
- INDEX `idx_consumos_tenant_recurso` (tenant_id, recurso)
- CHECK `periodo_fim > periodo_inicio`
- CHECK `quantidade_utilizada >= 0`

## `provedores_pagamento`

- UNIQUE `uq_provedores_codigo_ambiente` (codigo, ambiente)

## `faturas`

- UNIQUE `uq_faturas_numero` (numero)
- INDEX `idx_faturas_tenant_status` (tenant_id, status)
- INDEX `idx_faturas_status_vencimento` (status, vencimento)
- INDEX `idx_faturas_assinatura_id` (assinatura_id)
- CHECK `subtotal >= 0`
- CHECK `desconto >= 0`
- CHECK `valor_total >= 0`

## `pagamentos`

- UNIQUE `uq_pagamentos_chave_idempotencia` (chave_idempotencia)
- UNIQUE `uq_pagamentos_provedor_transacao` (provedor_pagamento_id, transacao_externa_id)
- INDEX `idx_pagamentos_tenant_status` (tenant_id, status)
- INDEX `idx_pagamentos_fatura_id` (fatura_id)
- CHECK `valor >= 0`

## `adicionais`

- UNIQUE `uq_adicionais_codigo` (codigo)
- CHECK `quantidade_recurso > 0`
- CHECK `valor >= 0`

## `cupons`

- UNIQUE `uq_cupons_codigo` (codigo)
- CHECK `valor_desconto > 0`
- CHECK `tipo_desconto <> 'percentual' OR valor_desconto <= 100`
- CHECK `valido_fim > valido_inicio`
- CHECK `quantidade_maxima IS NULL OR quantidade_maxima > 0`
- CHECK `quantidade_por_tenant IS NULL OR quantidade_por_tenant > 0`

## `cupons_utilizacoes`

- UNIQUE `uq_cupons_utilizacoes_cupom_fatura` (cupom_id, fatura_id)
- INDEX `idx_cupons_util_cupom_tenant` (cupom_id, tenant_id)
- INDEX `idx_cupons_utilizacoes_tenant_id` (tenant_id)
- INDEX `idx_cupons_utilizacoes_assinatura_id` (assinatura_id)
- INDEX `idx_cupons_utilizacoes_fatura_id` (fatura_id)
- CHECK `valor_desconto_aplicado >= 0`

## `faturas_itens`

- INDEX `idx_faturas_itens_tenant_fatura` (tenant_id, fatura_id)
- INDEX `idx_faturas_itens_fatura_id` (fatura_id)
- CHECK `quantidade > 0`
- CHECK `subtotal >= 0`
- CHECK `desconto >= 0`
- CHECK `valor_total >= 0`

## `assinaturas_historicos`

- INDEX `idx_assinaturas_hist_tenant_assinatura` (tenant_id, assinatura_id)
- INDEX `idx_assinaturas_historicos_assinatura_id` (assinatura_id)

## `assinaturas_alteracoes`

- INDEX `idx_assinaturas_alt_tenant_assinatura` (tenant_id, assinatura_id)
- INDEX `idx_assinaturas_alteracoes_assinatura_id` (assinatura_id)
- INDEX `idx_assinaturas_alteracoes_plano_versao_origem_id` (plano_versao_origem_id)
- INDEX `idx_assinaturas_alteracoes_plano_versao_destino_id` (plano_versao_destino_id)

## `pagamentos_eventos`

- UNIQUE `uq_pagamentos_eventos_provedor_chave` (provedor_pagamento_id, chave_deduplicacao)
- INDEX `idx_pagamentos_eventos_status` (status_processamento, recebido_em)
- INDEX `idx_pagamentos_eventos_tenant_id` (tenant_id)
- CHECK `tentativas >= 0`

## `pagamentos_reembolsos`

- UNIQUE `uq_reembolsos_pagamento_externo` (pagamento_id, reembolso_externo_id)
- INDEX `idx_reembolsos_tenant_status` (tenant_id, status)
- CHECK `valor > 0`

## `consumos_eventos`

- UNIQUE `uq_consumos_eventos_tenant_chave` (tenant_id, chave_idempotencia)
- INDEX `idx_consumos_eventos_assinatura_rec` (assinatura_id, recurso, ocorrido_em)
- INDEX `idx_consumos_eventos_evento_compensado_id` (evento_compensado_id)
- CHECK `quantidade <> 0`

## `tenants_beneficios`

- INDEX `idx_tenants_beneficios_tenant_fim` (tenant_id, fim)
- INDEX `idx_tenants_beneficios_funcionalidade_id` (funcionalidade_id)
- CHECK `recurso IS NOT NULL OR funcionalidade_id IS NOT NULL`
- CHECK `fim IS NULL OR fim > inicio`
- CHECK `quantidade_extra IS NULL OR quantidade_extra > 0`

## `planos_adicionais`

- UNIQUE `uq_planos_adicionais_versao_adicional` (plano_versao_id, adicional_id)
- INDEX `idx_planos_adicionais_adicional_id` (adicional_id)
- CHECK `quantidade_maxima IS NULL OR quantidade_maxima > 0`

## `planos_precos_provedores`

- UNIQUE `uq_precos_provedores_provedor_externo` (provedor_pagamento_id, preco_externo_id)
- INDEX `idx_precos_provedores_preco` (plano_preco_id, provedor_pagamento_id)

## Unicidade condicional e valores nulos

PostgreSQL e SQLite aceitam `uq_assinaturas_tenant_efetiva` como índice parcial. No SQL Server, usar índice filtrado. No MySQL, usar coluna gerada que seja `tenant_id` nos status efetivos e NULL nos demais, com índice único nela, sem alterar o nome lógico da regra. Registrar a escolha no mapeamento e testá-la sob concorrência.

Unicidades com coluna anulável permitem várias linhas com NULL. Isso é intencional em `transacao_externa_id`, `assinatura_externa_id`, `reembolso_externo_id` e `fatura_id`. O controle de cupom sem fatura é transacional, conforme `regras-financeiras.md`.
