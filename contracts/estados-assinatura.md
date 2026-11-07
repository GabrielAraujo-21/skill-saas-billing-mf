# Estados da assinatura

> Arquivo gerado por `scripts/gerar_documentos.py` a partir de `schema-manifest.yaml`. Não editar à mão.

- **Iniciais:** pendente, trial.
- **Efetivos (no máximo um por tenant):** pendente, trial, ativa, inadimplente, suspensa, cancelamento_agendado.
- **Terminais:** cancelada, expirada. Reativar depois deles cria nova assinatura.

## Transições permitidas

| De | Para | Gatilho |
|---|---|---|
| `pendente` | `ativa` | Pagamento confirmado por evento verificado do provedor ou plano sem cobrança. |
| `pendente` | `cancelada` | Desistência antes da confirmação. |
| `pendente` | `expirada` | Prazo de confirmação encerrado. |
| `trial` | `ativa` | Conversão confirmada por evento verificado ou plano sem cobrança. |
| `trial` | `cancelada` | Cancelamento durante o trial. |
| `trial` | `expirada` | Fim do trial sem conversão. |
| `ativa` | `inadimplente` | Falha de cobrança ou fatura vencida confirmada. |
| `ativa` | `cancelamento_agendado` | Cancelamento solicitado para o fim do período. |
| `ativa` | `cancelada` | Cancelamento imediato autorizado. |
| `inadimplente` | `ativa` | Regularização confirmada. |
| `inadimplente` | `suspensa` | Fim da tolerância definida em ADR. |
| `inadimplente` | `cancelada` | Cancelamento solicitado ou política de inadimplência. |
| `suspensa` | `ativa` | Regularização confirmada. |
| `suspensa` | `cancelada` | Cancelamento solicitado ou política de inadimplência. |
| `suspensa` | `expirada` | Fim do prazo de retenção da suspensão. |
| `cancelamento_agendado` | `ativa` | Desistência do cancelamento antes do fim do período. |
| `cancelamento_agendado` | `cancelada` | Fim do período pago. |

Qualquer outra transição é recusada e registrada. Evento fora de ordem não regride um estado confirmado.

## Efeitos de acesso

| Estado | Efeito |
|---|---|
| `pendente` | Sem direitos pagos; somente regularizar o pagamento. |
| `trial` | Direitos da versão contratada até trial_fim, com os limites definidos em ADR. |
| `ativa` | Direitos integrais da versão contratada, itens e benefícios válidos. |
| `inadimplente` | Direitos mantidos durante a tolerância definida em ADR, com aviso. |
| `suspensa` | Leitura, exportação e regularização, conforme decisão comercial; sem novas operações. |
| `cancelamento_agendado` | Direitos integrais até periodo_fim. |
| `cancelada` | Sem uso; exportação conforme contrato, lei e retenção. |
| `expirada` | Sem uso; exportação conforme contrato, lei e retenção. |

O efeito define o teto comercial; a permissão do usuário continua vindo de RBAC/ABAC.
