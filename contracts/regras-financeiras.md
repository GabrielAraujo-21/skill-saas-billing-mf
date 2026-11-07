# Regras financeiras

Regras normativas do contrato. O que depender de decisão comercial do projeto vai para ADR, sem alterar estas regras.

## Dinheiro

- Banco: `decimal(12,2)`. API: string com duas casas. Float é proibido em qualquer etapa.
- Moeda ISO 4217 em maiúsculas. O contrato 1.0.0 cobre moedas de duas casas; outra escala exige ADR e nova versão.
- Arredondamento meio para cima em duas casas, por linha, antes de somar. Assim, o total confere com a soma dos itens.
- `faturas.valor_total = subtotal - desconto`, e nunca fica negativo. O serviço valida essa conta na mesma transação.

## Três valores que não se confundem

| Valor | Onde fica | Muda quando |
|---|---|---|
| Preço de catálogo | `planos_precos.valor` | Nunca: nova versão do plano |
| Preço contratado | `assinaturas.valor_contratado`, `assinaturas_itens.valor_unitario` | Alteração contratual registrada |
| Valor cobrado | `faturas.valor_total`, `pagamentos.valor` | Lançamento próprio, nunca edição |

## Versões do catálogo

- Só `rascunho` pode ser editada. `publicada` é imutável em preços, funcionalidades e limites.
- Em `sob_consulta`, `valor` fica nulo e o plano não passa por checkout automático; o valor negociado vai para `valor_contratado`.
- Em `a_partir_de`, `valor` é o preço de entrada exibido, e `valor_contratado` guarda o acordado.
- Plano sem cobrança usa preço `fixo` com valor `0.00`, não gera fatura nem exige provedor, e renova o período para medir cotas.

## Direitos efetivos

`direitos = versão contratada + itens ativos + benefícios válidos`, limitados pelo efeito de acesso do estado atual. Cache precisa de invalidação na mudança de qualquer uma dessas partes. `limite` nulo significa ilimitado comercialmente, sempre sujeito a uso justo e limites técnicos; anúncio de `ilimitado` sem política de uso justo é proibido.

## Cobrança e idempotência

- Toda operação de cobrança tem `chave_idempotencia` com tenant e operação. Mesma chave com outro conteúdo é conflito.
- Não mantenha transação de banco aberta durante chamada ao provedor. Timeout não autoriza repetir: consulte e reconcilie.
- Webhook é gravado em `pagamentos_eventos`, com `chave_deduplicacao`, antes de responder sucesso. Processamento assíncrono, com retentativa limitada. Evento fora de ordem não regride estado confirmado.
- Reconciliação periódica cobre eventos perdidos, pendências e estornos.
- Uma fatura não aceita duas baixas confirmadas além do seu total.

## Trial

Duração em `planos_versoes.trial_dias`, com padrão zero. Uso repetido por tenant é bloqueado em transação. O fim do trial sem conversão leva a `expirada`, com os dados preservados.

## Mudança de plano e ciclo

Passa sempre por `assinaturas_alteracoes`. Upgrade, downgrade, troca de ciclo e prorrateamento dependem de ADR. O prorrateamento, quando adotado, é item próprio da fatura (`tipo_item = prorrateamento`). A mudança nunca gera dupla cobrança: fatura em aberto do período é ajustada ou compensada, não duplicada.

## Cupons

- Validade, limites e cumulatividade são conferidos e consumidos na mesma transação, no backend.
- Uma utilização por fatura, garantida por `uq_cupons_utilizacoes_cupom_fatura`. Sem fatura, a transação controla `quantidade_maxima` e `quantidade_por_tenant`.
- Desconto percentual vai de 0,01 a 100. O valor aplicado fica gravado, pois o cupom pode mudar depois.

## Consumo

`consumos_eventos` é a origem; `assinaturas_consumos` é o agregado reconciliável. Correção ocorre por evento compensatório com `evento_compensado_id`, nunca por recálculo silencioso. Limite é verificado e consumido de forma atômica.

## Reembolso e estorno

São lançamentos em `pagamentos_reembolsos`. O total reembolsado não passa de `pagamentos.valor`. Fatura e pagamento mudam de status por evento, sem apagar nada.

## Inadimplência e cancelamento

Tolerância, modo de leitura e prazos são decisão comercial em ADR. Cancelamento e inadimplência preservam acesso e exportação conforme contrato, lei e retenção; nenhum deles apaga dados automaticamente.

## Documentos fiscais

`faturas` é controle interno e não é documento fiscal. Obrigações fiscais exigem validação profissional no projeto.
