# Dicionário de dados

> Arquivo gerado por `scripts/gerar_documentos.py` a partir de `schema-manifest.yaml`. Não editar à mão.

## Convenções

- **nomes:** snake_case em pt-BR, sem acentos.
- **fuso_instantes:** UTC
- **datas_civis:** Colunas date não sofrem conversão de fuso.
- **moeda:** ISO 4217, maiúscula; catálogo validado para moedas com duas casas.
- **dinheiro:** decimal(12,2) em banco e string na API; float é proibido.
- **arredondamento:** Meio para cima (half-up) em duas casas, aplicado por linha antes de somar.
- **fk_padrao:** ON DELETE RESTRICT e ON UPDATE RESTRICT.
- **tenant_em_filhas:** Toda linha com tenant_id deve pertencer ao mesmo tenant das linhas referenciadas, por FK composta ou validação transacional.

## Enumerações

| Enumeração | Valores |
|---|---|
| `status_versao` | `rascunho`, `publicada`, `encerrada` |
| `periodicidade_preco` | `mensal`, `anual` |
| `periodicidade_adicional` | `mensal`, `anual`, `avulso` |
| `periodicidade_limite` | `mensal`, `anual`, `sem_periodo` |
| `modalidade_preco` | `fixo`, `a_partir_de`, `sob_consulta` |
| `status_assinatura` | `pendente`, `trial`, `ativa`, `inadimplente`, `suspensa`, `cancelamento_agendado`, `cancelada`, `expirada` |
| `ambiente` | `sandbox`, `producao` |
| `status_fatura` | `rascunho`, `aberta`, `paga`, `vencida`, `cancelada`, `reembolsada` |
| `status_pagamento` | `pendente`, `confirmado`, `falhou`, `cancelado`, `reembolsado_parcial`, `reembolsado`, `contestado` |
| `metodo_pagamento` | `cartao`, `pix`, `pix_automatico`, `boleto` |
| `tipo_desconto` | `percentual`, `valor_fixo` |
| `tipo_item_fatura` | `plano`, `adicional`, `implantacao`, `prorrateamento`, `ajuste` |
| `tipo_evento_historico` | `criacao`, `transicao_status`, `renovacao`, `alteracao_plano`, `alteracao_item`, `cancelamento`, `ajuste_manual` |
| `tipo_alteracao` | `upgrade`, `downgrade`, `troca_periodicidade`, `troca_provedor` |
| `status_alteracao` | `solicitada`, `agendada`, `efetivada`, `cancelada`, `falhou` |
| `status_processamento_evento` | `recebido`, `processando`, `processado`, `ignorado`, `falhou` |
| `status_reembolso` | `solicitado`, `processando`, `concluido`, `falhou`, `cancelado` |
| `tipo_beneficio` | `cota_extra`, `funcionalidade`, `cortesia` |
| `status_preco_provedor` | `pendente`, `sincronizado`, `erro`, `desativado` |

## 1. `planos`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `nome` | varchar(100) | não | — | — | — |
| `slug` | varchar(100) | não | — | — | — |
| `descricao` | text | sim | — | — | — |
| `publico_alvo` | varchar(255) | sim | — | — | — |
| `destaque` | boolean | não | false | — | — |
| `publico` | boolean | não | false | — | — |
| `ativo` | boolean | não | true | — | — |
| `ordem_exibicao` | int | não | 0 | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |
| `deleted_at` | timestamp | sim | — | — | — |

## 2. `planos_versoes`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `plano_id` | bigint | não | — | — | — |
| `numero_versao` | int | não | — | — | — |
| `nome_versao` | varchar(100) | não | — | — | — |
| `status` | varchar(30) | não | rascunho | status_versao | — |
| `vigencia_inicio` | timestamp | sim | — | — | — |
| `vigencia_fim` | timestamp | sim | — | — | — |
| `trial_dias` | int | não | 0 | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 3. `planos_precos`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `plano_versao_id` | bigint | não | — | — | — |
| `periodicidade` | varchar(20) | não | — | periodicidade_preco | — |
| `moeda` | char(3) | não | — | — | — |
| `modalidade_preco` | varchar(20) | não | fixo | modalidade_preco | Acréscimo ao prompt: cobre valor de entrada e preço sob consulta. |
| `valor` | decimal(12,2) | sim | — | — | NULL somente com modalidade_preco = sob_consulta. |
| `valor_implantacao` | decimal(12,2) | não | 0.00 | — | — |
| `ativo` | boolean | não | true | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 4. `funcionalidades`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `codigo` | varchar(100) | não | — | — | Código durável, como integracoes.api. |
| `nome` | varchar(150) | não | — | — | — |
| `descricao` | text | sim | — | — | — |
| `categoria` | varchar(100) | sim | — | — | — |
| `ativo` | boolean | não | true | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 5. `planos_funcionalidades`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `plano_versao_id` | bigint | não | — | — | — |
| `funcionalidade_id` | bigint | não | — | — | — |
| `habilitado` | boolean | não | true | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 6. `planos_limites`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `plano_versao_id` | bigint | não | — | — | — |
| `recurso` | varchar(100) | não | — | — | — |
| `limite` | bigint | sim | — | — | NULL = ilimitado comercialmente, sujeito a uso justo e limites técnicos. |
| `periodicidade` | varchar(20) | não | sem_periodo | periodicidade_limite | NOT NULL para a unicidade valer em todo SGBD. |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 7. `assinaturas`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `tenant_id` | bigint | não | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `plano_versao_id` | bigint | não | — | — | — |
| `plano_preco_id` | bigint | não | — | — | — |
| `provedor_pagamento_id` | bigint | sim | — | — | — |
| `assinatura_externa_id` | varchar(255) | sim | — | — | — |
| `status` | varchar(30) | não | — | status_assinatura | — |
| `periodicidade` | varchar(20) | não | — | periodicidade_preco | — |
| `valor_contratado` | decimal(12,2) | não | — | — | — |
| `moeda` | char(3) | não | — | — | — |
| `trial_inicio` | timestamp | sim | — | — | — |
| `trial_fim` | timestamp | sim | — | — | — |
| `periodo_inicio` | timestamp | não | — | — | — |
| `periodo_fim` | timestamp | não | — | — | — |
| `proxima_cobranca_em` | timestamp | sim | — | — | — |
| `cancelamento_solicitado_em` | timestamp | sim | — | — | — |
| `cancelado_em` | timestamp | sim | — | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 8. `assinaturas_itens`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `tenant_id` | bigint | não | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `assinatura_id` | bigint | não | — | — | — |
| `adicional_id` | bigint | não | — | — | — |
| `quantidade` | int | não | — | — | — |
| `valor_unitario` | decimal(12,2) | não | — | — | Snapshot na contratação. |
| `valor_total` | decimal(12,2) | não | — | — | Snapshot na contratação. |
| `periodicidade` | varchar(20) | não | — | periodicidade_adicional | — |
| `ativo` | boolean | não | true | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 9. `assinaturas_consumos`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `tenant_id` | bigint | não | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `assinatura_id` | bigint | não | — | — | — |
| `recurso` | varchar(100) | não | — | — | — |
| `periodo_inicio` | timestamp | não | — | — | — |
| `periodo_fim` | timestamp | não | — | — | — |
| `quantidade_utilizada` | bigint | não | 0 | — | — |
| `ultima_atualizacao_em` | timestamp | sim | — | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 10. `provedores_pagamento`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `nome` | varchar(100) | não | — | — | — |
| `codigo` | varchar(50) | não | — | — | — |
| `ambiente` | varchar(20) | não | — | ambiente | — |
| `ativo` | boolean | não | true | — | — |
| `configuracao_referencia` | varchar(255) | sim | — | — | Só o nome da configuração ou do cofre; nunca a credencial. |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 11. `faturas`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `tenant_id` | bigint | não | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `assinatura_id` | bigint | não | — | — | — |
| `numero` | varchar(50) | não | — | — | — |
| `competencia` | date | não | — | — | Data civil, sem conversão de fuso. |
| `vencimento` | date | não | — | — | Data civil, sem conversão de fuso. |
| `subtotal` | decimal(12,2) | não | — | — | — |
| `desconto` | decimal(12,2) | não | 0.00 | — | — |
| `valor_total` | decimal(12,2) | não | — | — | — |
| `moeda` | char(3) | não | — | — | — |
| `status` | varchar(30) | não | — | status_fatura | — |
| `pago_em` | timestamp | sim | — | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 12. `pagamentos`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `tenant_id` | bigint | não | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `fatura_id` | bigint | não | — | — | — |
| `provedor_pagamento_id` | bigint | não | — | — | — |
| `transacao_externa_id` | varchar(255) | sim | — | — | — |
| `chave_idempotencia` | varchar(255) | não | — | — | Deve incluir tenant e operação, pois a unicidade é global. |
| `metodo_pagamento` | varchar(30) | não | — | metodo_pagamento | — |
| `valor` | decimal(12,2) | não | — | — | — |
| `moeda` | char(3) | não | — | — | — |
| `status` | varchar(30) | não | — | status_pagamento | — |
| `pago_em` | timestamp | sim | — | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 13. `adicionais`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `codigo` | varchar(100) | não | — | — | — |
| `nome` | varchar(150) | não | — | — | — |
| `descricao` | text | sim | — | — | — |
| `recurso` | varchar(100) | não | — | — | — |
| `quantidade_recurso` | bigint | não | — | — | — |
| `valor` | decimal(12,2) | não | — | — | — |
| `periodicidade` | varchar(20) | não | — | periodicidade_adicional | — |
| `ativo` | boolean | não | true | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 14. `cupons`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `codigo` | varchar(50) | não | — | — | — |
| `descricao` | varchar(255) | sim | — | — | — |
| `tipo_desconto` | varchar(20) | não | — | tipo_desconto | — |
| `valor_desconto` | decimal(12,2) | não | — | — | — |
| `quantidade_maxima` | int | sim | — | — | — |
| `quantidade_por_tenant` | int | sim | — | — | — |
| `valido_inicio` | timestamp | não | — | — | — |
| `valido_fim` | timestamp | não | — | — | — |
| `ativo` | boolean | não | true | — | — |
| `cumulativo` | boolean | não | false | — | Acréscimo ao prompt: regra de cumulatividade. |
| `planos_elegiveis` | json | sim | — | — | Acréscimo: slugs de plano; NULL = todos. |
| `periodicidades_elegiveis` | json | sim | — | — | Acréscimo: ciclos permitidos; NULL = todos. |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 15. `cupons_utilizacoes`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `cupom_id` | bigint | não | — | — | — |
| `tenant_id` | bigint | não | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `assinatura_id` | bigint | não | — | — | — |
| `fatura_id` | bigint | sim | — | — | — |
| `valor_desconto_aplicado` | decimal(12,2) | não | — | — | — |
| `utilizado_em` | timestamp | não | — | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 16. `faturas_itens`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `tenant_id` | bigint | não | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `fatura_id` | bigint | não | — | — | — |
| `tipo_item` | varchar(30) | não | — | tipo_item_fatura | — |
| `referencia_id` | bigint | sim | — | — | Referência lógica conforme tipo_item, sem FK. |
| `descricao` | varchar(255) | não | — | — | — |
| `quantidade` | int | não | — | — | — |
| `valor_unitario` | decimal(12,2) | não | — | — | — |
| `subtotal` | decimal(12,2) | não | — | — | — |
| `desconto` | decimal(12,2) | não | 0.00 | — | — |
| `valor_total` | decimal(12,2) | não | — | — | — |
| `moeda` | char(3) | não | — | — | — |
| `ordem` | int | não | 0 | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 17. `assinaturas_historicos`

Exceção de timestamps: Registro imutável: não há atualização, logo não há updated_at.

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `tenant_id` | bigint | não | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `assinatura_id` | bigint | não | — | — | — |
| `tipo_evento` | varchar(30) | não | — | tipo_evento_historico | — |
| `status_anterior` | varchar(30) | sim | — | status_assinatura | — |
| `status_novo` | varchar(30) | sim | — | status_assinatura | — |
| `dados_anteriores` | json | sim | — | — | — |
| `dados_novos` | json | sim | — | — | — |
| `ator_id` | bigint | sim | — | — | Usuário ou processo; FK real definida no mapeamento. |
| `ocorrido_em` | timestamp | não | — | — | — |
| `correlacao_id` | varchar(100) | sim | — | — | — |
| `created_at` | timestamp | não | — | — | — |

## 18. `assinaturas_alteracoes`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `tenant_id` | bigint | não | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `assinatura_id` | bigint | não | — | — | — |
| `tipo_alteracao` | varchar(30) | não | — | tipo_alteracao | — |
| `plano_versao_origem_id` | bigint | sim | — | — | — |
| `plano_versao_destino_id` | bigint | sim | — | — | — |
| `efetivacao_em` | timestamp | sim | — | — | — |
| `prorrateamento_valor` | decimal(12,2) | sim | — | — | Pode ser negativo quando gera crédito. |
| `status` | varchar(30) | não | — | status_alteracao | — |
| `solicitado_em` | timestamp | não | — | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 19. `pagamentos_eventos`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `provedor_pagamento_id` | bigint | não | — | — | — |
| `tenant_id` | bigint | sim | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `evento_externo_id` | varchar(255) | sim | — | — | — |
| `chave_deduplicacao` | varchar(255) | não | — | — | ID do provedor quando garantido; senão hash SHA-256 do evento canônico. |
| `tipo` | varchar(100) | não | — | — | — |
| `payload_referencia` | varchar(255) | sim | — | — | Referência a armazenamento restrito; sem dados sensíveis. |
| `assinatura_externa_id` | varchar(255) | sim | — | — | — |
| `recebido_em` | timestamp | não | — | — | — |
| `processado_em` | timestamp | sim | — | — | — |
| `status_processamento` | varchar(30) | não | recebido | status_processamento_evento | — |
| `tentativas` | int | não | 0 | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 20. `pagamentos_reembolsos`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `tenant_id` | bigint | não | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `pagamento_id` | bigint | não | — | — | — |
| `reembolso_externo_id` | varchar(255) | sim | — | — | — |
| `valor` | decimal(12,2) | não | — | — | — |
| `moeda` | char(3) | não | — | — | — |
| `motivo` | varchar(255) | sim | — | — | — |
| `status` | varchar(30) | não | — | status_reembolso | — |
| `solicitado_em` | timestamp | não | — | — | — |
| `concluido_em` | timestamp | sim | — | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 21. `consumos_eventos`

Exceção de timestamps: Evento imutável: correção por evento de compensação, nunca por atualização.

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `tenant_id` | bigint | não | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `assinatura_id` | bigint | não | — | — | — |
| `recurso` | varchar(100) | não | — | — | — |
| `quantidade` | bigint | não | — | — | Negativa apenas em compensação. |
| `ocorrido_em` | timestamp | não | — | — | — |
| `chave_idempotencia` | varchar(255) | não | — | — | — |
| `origem` | varchar(100) | sim | — | — | — |
| `evento_compensado_id` | bigint | sim | — | — | Acréscimo: liga a compensação ao evento original. |
| `created_at` | timestamp | não | — | — | — |

## 22. `tenants_beneficios`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `tenant_id` | bigint | não | — | — | Tenant já existente no projeto; tipo e tabela reais vão no mapeamento. |
| `recurso` | varchar(100) | sim | — | — | — |
| `funcionalidade_id` | bigint | sim | — | — | — |
| `tipo_beneficio` | varchar(30) | não | — | tipo_beneficio | — |
| `quantidade_extra` | bigint | sim | — | — | — |
| `inicio` | timestamp | não | — | — | — |
| `fim` | timestamp | sim | — | — | — |
| `justificativa` | varchar(500) | não | — | — | — |
| `concedido_por` | bigint | sim | — | — | FK real definida no mapeamento. |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 23. `planos_adicionais`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `plano_versao_id` | bigint | não | — | — | — |
| `adicional_id` | bigint | não | — | — | — |
| `habilitado` | boolean | não | true | — | — |
| `quantidade_maxima` | int | sim | — | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |

## 24. `planos_precos_provedores`

| Coluna | Tipo | Nulo | Padrão | Enum | Nota |
|---|---|---|---|---|---|
| `id` | bigint | não | — | — | Chave primária; outro tipo só por ADR de chaves. |
| `plano_preco_id` | bigint | não | — | — | — |
| `provedor_pagamento_id` | bigint | não | — | — | A linha do provedor já identifica o ambiente. |
| `preco_externo_id` | varchar(255) | não | — | — | — |
| `status` | varchar(30) | não | pendente | status_preco_provedor | — |
| `sincronizado_em` | timestamp | sim | — | — | — |
| `created_at` | timestamp | não | — | — | — |
| `updated_at` | timestamp | não | — | — | — |
