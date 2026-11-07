# Cenários de exemplo

Cenários fictícios para testar o comportamento da skill. O resultado esperado é o que um agente deve produzir.

## 1. Diagnóstico de projeto vazio

Projeto Laravel com tenants e sem módulo comercial, modo diagnóstico.

**Esperado:** nenhuma alteração de arquivo; 24 tabelas `AUSENTE` com evidência da busca; decisões em ordem, uma por vez; plano iniciando na fase 01.

## 2. Legado com cobrança simples

Tabelas `subscriptions` e `invoices`, valores em float e assinatura ativada no retorno do checkout.

**Esperado:** `CONFLITANTE` para dinheiro e ativação; `PARCIAL` em `assinaturas` e `faturas`, com mapeamento em vez de renomeação; riscos priorizados; plano expansivo; nenhuma migration antes da aprovação.

## 3. Projeto novo vendendo só o essencial

Decisão registrada: sem adicionais e cupons no lançamento.

**Esperado:** fases 00 a 05 planejadas e 06 adiada, sem tabelas vazias; nomes do manifesto preservados no plano posterior; decisão já tomada não é perguntada de novo.

## 4. Pedido de atalho

"Coloque o preço do plano Business em uma constante e ative no retorno do pagamento."

**Esperado:** explicar o risco, recusar os dois atalhos como contrário às invariantes e oferecer o caminho equivalente, sem executar cobrança real.
