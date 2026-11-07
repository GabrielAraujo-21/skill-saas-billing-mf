# Aplicação em projeto novo

Modo `projeto_novo`: o esquema segue o manifesto exatamente. Só IDs, tenants e técnicas do SGBD podem ir para o mapeamento.

1. Confirme que a identidade de tenants existe. Se não existir, resolva primeiro com `skill-backend-mf`; o módulo depende dela.
2. Leve as decisões do [fluxo consultivo](fluxo-consultivo.md) que afetam a fase.
3. Registre versão e checksum no [registro de aplicação](../templates/registro-aplicacao.yaml).
4. Escreva o ADR da fase e aguarde aprovação.
5. Gere migrations, models, serviços, policies, validações, testes, OpenAPI e documentação **só da fase aprovada**. Traduza do manifesto: nome, tipo, nulidade, padrão, FK, índice e CHECK.
6. Adicione o teste de aderência que compara banco e manifesto, descrito em [compatibilidade](../contracts/contratos-compatibilidade.md).
7. Se precisar de dados iniciais, use o [seed de exemplo](../templates/seed-planos-exemplo.md) apenas fora de produção ou com preços aprovados.
8. Verifique com os [critérios de aceitação](criterios-aceitacao.md) e atualize as pendências.

Migrations criam as tabelas na ordem do [catálogo](../contracts/catalogo-tabelas.md); dentro de uma fase, a tabela referenciada vem antes. Não execute migration em ambiente real sem autorização específica.
