# Isolamento de tenants

Vale junto com a seção de multi-tenancy de `skill-backend-mf`. Se o projeto usa outra estratégia, como instalação dedicada, registre no mapeamento como `tenant_id` se aplica.

## Escopos do contrato

| Escopo | Tabelas | Regra |
|---|---|---|
| Global | Catálogo, provedores, adicionais, cupons | Sem `tenant_id`; gestão só no plano de controle |
| Tenant | Assinaturas, consumo, faturas, pagamentos e filhas | `tenant_id` obrigatório, escopo em toda consulta |
| Tenant opcional | `pagamentos_eventos` | Tenant desconhecido no recebimento; preenchido após correlação; visível só ao plano de controle até lá |

## Regras

- Sem contexto validado, leitura e gravação falham. Nada de fallback silencioso.
- `tenant_id` vem do contexto autenticado, nunca do corpo da requisição.
- Linha filha tem o mesmo tenant da linha pai. Use FK composta (`tenant_id`, `assinatura_id`) quando o SGBD e o projeto permitirem, ou valide na transação e teste.
- Tenant participa de cache, locks, chaves de idempotência, filas, exportações e logs.
- Job recebe tenant e identificadores simples, estabelece o contexto antes de buscar modelos e o limpa ao terminar.
- Webhook não tem tenant de sessão: é resolvido pela assinatura ou transação externa, com o provedor e o ambiente daquela rota. Se não houver correlação, o evento fica retido para análise, sem efeito.
- Operador da plataforma não tem acesso irrestrito. Operações entre tenants exigem caso de uso, autorização e auditoria.

## Testes negativos mínimos

Para cada recurso por tenant: leitura, listagem, atualização, exportação e anexo com ID de outro tenant são negados sem revelar existência. Inclua FK cruzada, como assinatura do tenant A em fatura do tenant B.
