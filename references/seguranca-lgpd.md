# Segurança e LGPD

Estas regras orientam a engenharia e não substituem avaliação jurídica. Base legal, prazos de retenção, termos e obrigações fiscais precisam de validação profissional no projeto.

## Segurança

- Negação por padrão em toda rota comercial. Gestão de preços, cupons e benefícios exige papel específico e trilha de quem, quando e por quê.
- Nunca armazene PAN nem CVV. Nunca coloque segredo no repositório, em log, em analytics ou no bundle do frontend.
- `pagamentos_eventos` e payloads brutos têm acesso restrito, retenção explícita e minimização.
- Limite as rotas públicas e de webhook contra abuso. Valide cupom sem permitir enumeração.
- Desconto manual, benefício e reembolso exigem justificativa e autorização.
- Trial e cupom têm proteção contra abuso por tenant, sem depender de checagem no navegador.

## LGPD

| Tema | Aplicação |
|---|---|
| Minimização | Gravar só o necessário para cobrar e auditar |
| Finalidade | Dados de cobrança não servem a outro uso sem base própria |
| Acesso | Restrito e auditado; operador da plataforma vê o mínimo |
| Retenção | Prazo por tipo de dado, com rotina de descarte |
| Direitos do titular | Exportação e correção; exclusão compatível com obrigações legais |
| Incidente | Procedimento definido, e logs sem dado sensível |

Registro financeiro pode precisar ser mantido por obrigação legal mesmo após pedido de exclusão. Nesses casos, separe ou anonimize o que for possível, em vez de apagar a trilha, conforme orientação jurídica.
