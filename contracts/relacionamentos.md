# Relacionamentos

> Arquivo gerado por `scripts/gerar_documentos.py` a partir de `schema-manifest.yaml`. Não editar à mão.

| Tabela | Coluna | Referencia | Nulo | ON DELETE | ON UPDATE |
|---|---|---|---|---|---|
| `planos_versoes` | `plano_id` | `planos.id` | não | RESTRICT | RESTRICT |
| `planos_precos` | `plano_versao_id` | `planos_versoes.id` | não | RESTRICT | RESTRICT |
| `planos_funcionalidades` | `plano_versao_id` | `planos_versoes.id` | não | RESTRICT | RESTRICT |
| `planos_funcionalidades` | `funcionalidade_id` | `funcionalidades.id` | não | RESTRICT | RESTRICT |
| `planos_limites` | `plano_versao_id` | `planos_versoes.id` | não | RESTRICT | RESTRICT |
| `assinaturas` | `tenant_id` | `tenants.id` | não | RESTRICT | RESTRICT |
| `assinaturas` | `plano_versao_id` | `planos_versoes.id` | não | RESTRICT | RESTRICT |
| `assinaturas` | `plano_preco_id` | `planos_precos.id` | não | RESTRICT | RESTRICT |
| `assinaturas` | `provedor_pagamento_id` | `provedores_pagamento.id` | sim | RESTRICT | RESTRICT |
| `assinaturas_itens` | `tenant_id` | `tenants.id` | não | RESTRICT | RESTRICT |
| `assinaturas_itens` | `assinatura_id` | `assinaturas.id` | não | RESTRICT | RESTRICT |
| `assinaturas_itens` | `adicional_id` | `adicionais.id` | não | RESTRICT | RESTRICT |
| `assinaturas_consumos` | `tenant_id` | `tenants.id` | não | RESTRICT | RESTRICT |
| `assinaturas_consumos` | `assinatura_id` | `assinaturas.id` | não | RESTRICT | RESTRICT |
| `faturas` | `tenant_id` | `tenants.id` | não | RESTRICT | RESTRICT |
| `faturas` | `assinatura_id` | `assinaturas.id` | não | RESTRICT | RESTRICT |
| `pagamentos` | `tenant_id` | `tenants.id` | não | RESTRICT | RESTRICT |
| `pagamentos` | `fatura_id` | `faturas.id` | não | RESTRICT | RESTRICT |
| `pagamentos` | `provedor_pagamento_id` | `provedores_pagamento.id` | não | RESTRICT | RESTRICT |
| `cupons_utilizacoes` | `cupom_id` | `cupons.id` | não | RESTRICT | RESTRICT |
| `cupons_utilizacoes` | `tenant_id` | `tenants.id` | não | RESTRICT | RESTRICT |
| `cupons_utilizacoes` | `assinatura_id` | `assinaturas.id` | não | RESTRICT | RESTRICT |
| `cupons_utilizacoes` | `fatura_id` | `faturas.id` | sim | RESTRICT | RESTRICT |
| `faturas_itens` | `tenant_id` | `tenants.id` | não | RESTRICT | RESTRICT |
| `faturas_itens` | `fatura_id` | `faturas.id` | não | RESTRICT | RESTRICT |
| `assinaturas_historicos` | `tenant_id` | `tenants.id` | não | RESTRICT | RESTRICT |
| `assinaturas_historicos` | `assinatura_id` | `assinaturas.id` | não | RESTRICT | RESTRICT |
| `assinaturas_alteracoes` | `tenant_id` | `tenants.id` | não | RESTRICT | RESTRICT |
| `assinaturas_alteracoes` | `assinatura_id` | `assinaturas.id` | não | RESTRICT | RESTRICT |
| `assinaturas_alteracoes` | `plano_versao_origem_id` | `planos_versoes.id` | sim | RESTRICT | RESTRICT |
| `assinaturas_alteracoes` | `plano_versao_destino_id` | `planos_versoes.id` | sim | RESTRICT | RESTRICT |
| `pagamentos_eventos` | `provedor_pagamento_id` | `provedores_pagamento.id` | não | RESTRICT | RESTRICT |
| `pagamentos_eventos` | `tenant_id` | `tenants.id` | sim | RESTRICT | RESTRICT |
| `pagamentos_reembolsos` | `tenant_id` | `tenants.id` | não | RESTRICT | RESTRICT |
| `pagamentos_reembolsos` | `pagamento_id` | `pagamentos.id` | não | RESTRICT | RESTRICT |
| `consumos_eventos` | `tenant_id` | `tenants.id` | não | RESTRICT | RESTRICT |
| `consumos_eventos` | `assinatura_id` | `assinaturas.id` | não | RESTRICT | RESTRICT |
| `consumos_eventos` | `evento_compensado_id` | `consumos_eventos.id` | sim | RESTRICT | RESTRICT |
| `tenants_beneficios` | `tenant_id` | `tenants.id` | não | RESTRICT | RESTRICT |
| `tenants_beneficios` | `funcionalidade_id` | `funcionalidades.id` | sim | RESTRICT | RESTRICT |
| `planos_adicionais` | `plano_versao_id` | `planos_versoes.id` | não | RESTRICT | RESTRICT |
| `planos_adicionais` | `adicional_id` | `adicionais.id` | não | RESTRICT | RESTRICT |
| `planos_precos_provedores` | `plano_preco_id` | `planos_precos.id` | não | RESTRICT | RESTRICT |
| `planos_precos_provedores` | `provedor_pagamento_id` | `provedores_pagamento.id` | não | RESTRICT | RESTRICT |

## Referências sem FK no contrato

| Tabela | Coluna | Destino |
|---|---|---|
| `assinaturas_historicos` | `ator_id` | usuarios, definido no mapeamento |
| `tenants_beneficios` | `concedido_por` | usuarios, definido no mapeamento |
