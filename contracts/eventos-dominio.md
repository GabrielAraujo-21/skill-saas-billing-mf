# Eventos de domínio

Eventos internos do módulo. O nome é contrato; a publicação (síncrona, fila ou outbox) é decidida em ADR. Eventos que afetam dinheiro ou direitos são publicados somente após o commit.

## Envelope

| Campo | Regra |
|---|---|
| `evento` | Nome abaixo |
| `versao` | Inteiro, começando em 1 |
| `ocorrido_em` | Instante ISO 8601 em UTC |
| `tenant_id` | Obrigatório, exceto em eventos de catálogo |
| `correlacao_id` | Mesmo valor de toda a cadeia |
| `dados` | Só identificadores e valores necessários; sem dado de cartão, credencial ou payload bruto |

## Catálogo

`plano.versao_publicada`, `plano.versao_encerrada`

## Assinatura

`assinatura.criada`, `assinatura.ativada`, `assinatura.trial_iniciado`, `assinatura.trial_expirado`, `assinatura.inadimplente`, `assinatura.suspensa`, `assinatura.regularizada`, `assinatura.cancelamento_agendado`, `assinatura.cancelamento_revertido`, `assinatura.cancelada`, `assinatura.expirada`, `assinatura.alteracao_solicitada`, `assinatura.alteracao_efetivada`

Cada transição também grava `assinaturas_historicos`, na mesma transação.

## Consumo

`consumo.registrado`, `consumo.compensado`, `consumo.limiar_atingido`, `consumo.limite_excedido`, `beneficio.concedido`, `beneficio.expirado`

## Financeiro

`fatura.emitida`, `fatura.paga`, `fatura.vencida`, `fatura.cancelada`, `pagamento.confirmado`, `pagamento.falhou`, `pagamento.contestado`, `reembolso.solicitado`, `reembolso.concluido`, `webhook.recebido`, `webhook.rejeitado`, `reconciliacao.divergencia`

## Monetização complementar

`adicional.contratado`, `adicional.encerrado`, `cupom.aplicado`, `cupom.recusado`

## Regras de consumo

Consumidores são idempotentes e toleram duplicidade e reordenação. Evento nunca é fonte de autorização: quem o recebe em outro módulo consulta os direitos efetivos.
