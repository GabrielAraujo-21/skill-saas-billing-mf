# Critérios de aceitação

Mínimo no projeto consumidor, proporcional às fases aplicadas. Registre os resultados em [evidências de testes](../templates/evidencias-testes.md).

| Tema | Deve ser comprovado | Fase |
|---|---|---|
| Aderência | Banco confere com manifesto e mapeamento | Todas |
| Rollback | Migration reverte, ou há plano de recuperação sem perda | Todas |
| Tenancy cruzada | Acesso e FK de outro tenant são negados, sem revelar existência | 03+ |
| RBAC | Direito comercial não concede permissão; rotas negam por padrão | 02+ |
| Versão publicada | Preço e direitos não mudam; nova versão não afeta contrato vigente | 01 |
| Snapshot contratual | Editar catálogo não altera assinatura nem item | 03, 06 |
| Transições | Permitidas funcionam; proibidas são recusadas e registradas | 03 |
| Assinatura única | Duas contratações simultâneas resultam em uma efetiva | 03 |
| Ativação | Retorno do navegador não ativa; só evento verificado | 05 |
| Ciclo de cobrança | Renovação, falha e tolerância conforme ADR | 05 |
| Webhooks | Duplicado, fora de ordem e assinatura inválida, sem efeito indevido, sob concorrência | 05 |
| Cobrança idempotente | Repetição não duplica; mesma chave com outro conteúdo é conflito | 05 |
| Consumo | Concorrência não ultrapassa limite; evento repetido não soma duas vezes | 04 |
| Cupom | Expirado, esgotado e duplicado são recusados | 06 |
| Cancelamento | Agendado e imediato preservam acesso e exportação | 03, 05 |
| Mudança de plano | Upgrade e downgrade sem dupla cobrança | 03, 05 |
| Reembolso | Parcial e total são lançamentos; não passam do valor pago | 05 |
| API pública | Só publicados; nenhum campo interno; valida o OpenAPI | 01, 07 |
| Segredos | Nada sensível em log, resposta ou repositório | 05 |

Conclusão é bloqueada se falhar tenant, índice, integridade, idempotência ou contrato. Teste não executado é declarado como tal, nunca como aprovado.
