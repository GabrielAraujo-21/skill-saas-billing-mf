# Checklist de revisão

## Contrato

- [ ] Nomes, tipos, nulidade, padrões, FKs, índices e CHECKs conferem com o manifesto.
- [ ] Toda diferença está no mapeamento, com motivo e teste.
- [ ] Só tabelas da fase aprovada foram criadas.
- [ ] Nenhuma migration executada foi reescrita.

## Regras

- [ ] Direitos vêm só do serviço de direitos, sem plano fixo no código.
- [ ] Versão publicada é imutável, e o contrato vigente não muda.
- [ ] Mudança de status passa pelo serviço, com histórico na mesma transação.
- [ ] Dinheiro não usa float; API devolve string.
- [ ] Ativação só por evento verificado.

## Segurança

- [ ] Sem contexto de tenant, a operação falha; `tenant_id` nunca vem do payload.
- [ ] FK cruzada entre tenants é impedida e testada.
- [ ] Sem segredo, PAN, CVV ou payload sensível em código, log ou resposta.
- [ ] Webhook autenticado conforme a documentação oficial vigente.
- [ ] Direito comercial não concede permissão.

## Evidências

- [ ] Testes de sucesso e negativos executados, com saída registrada.
- [ ] O que não foi testado está declarado.
- [ ] Rollback descrito, e `PENDENCIAS.md` atualizado.
