# Provedores de pagamento

Esta referência fixa o padrão de integração, não detalhes de API. **Antes de implementar, leia a documentação oficial atual do produto**, pois endpoints, assinatura de webhook e recursos mudam, e não presuma equivalência entre provedores.

## Pontos de partida

- Mercado Pago: <https://www.mercadopago.com.br/developers/pt/docs/subscriptions/overview> e webhooks em <https://www.mercadopago.com.br/developers/pt/docs/subscriptions/additional-content/your-integrations/notifications/webhooks>
- Efí: <https://dev.efipay.com.br/docs/api-cobrancas/assinatura/> e notificações em <https://dev.efipay.com.br/docs/api-cobrancas/notificacoes/>

## O que comparar antes de escolher

| Critério | Pergunta |
|---|---|
| Recorrência | Cartão, boleto, Pix e Pix Automático funcionam em recorrência? Avalie cada um separadamente |
| Tentativas | Quem repete a cobrança após falha? |
| Webhook | Como autenticar? O ID do evento é único? |
| Testes | O sandbox simula renovação, falha e estorno? |
| Custos | Quais são as taxas por método e prazo, na proposta vigente? |
| Reembolso | Parcial e total são possíveis? Por API? |
| Reconciliação | Há consulta e listagem por período? |

## Padrão de implementação

- Um adaptador por provedor, atrás de contratos por capacidade.
- Uma linha em `provedores_pagamento` por provedor e ambiente, o que impede misturar IDs de sandbox e produção.
- Credenciais em cofre ou segredo do ambiente; `configuracao_referencia` guarda só a referência. Certificados fora do Git.
- Webhook: autenticar como o provedor exige, gravar em `pagamentos_eventos`, responder e processar em fila. Segredo em URL, sozinho, não é prova suficiente.
- `chave_deduplicacao`: o ID do provedor quando ele garantir unicidade; caso contrário, hash SHA-256 do evento canônico.
- Reconsulte o provedor quando o fluxo exigir, e não regrida estado confirmado.
- Retentativas limitadas com espera crescente, fila de falhas e alertas.
- Reconciliação periódica de perdidos, pendentes, resultados desconhecidos e estornos.
- Prefira checkout ou tokenização hospedados. Nunca armazene PAN ou CVV.

## Testes

Somente em sandbox, com autorização para contas externas. Cubra confirmação, recusa, duplicidade, fora de ordem, assinatura inválida, ambiente trocado e timeout. Produção exige autorização específica e nunca parte de seed.
