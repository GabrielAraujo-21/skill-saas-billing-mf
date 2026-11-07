---
name: skill-saas-billing-mf
description: Diagnosticar, planejar e implantar de forma padronizada o módulo comercial de um SaaS Laravel, com planos versionados, direitos de uso, limites, assinaturas, faturas, pagamentos, webhooks de PSP, consumo, adicionais e cupons, seguindo um contrato canônico de 24 tabelas. Usar sempre que o pedido envolver monetização, billing, cobrança recorrente, assinatura por tenant, entitlements, cotas, Mercado Pago, Efí ou aderência de um módulo comercial a esse contrato, mesmo sem citar a skill; não usar para pagamento avulso sem assinatura nem para trabalho exclusivamente de interface sem regra comercial.
metadata:
  version: "1.0.0"
---

# SaaS Billing MF

Esta skill leva qualquer SaaS Laravel compatível ao mesmo esquema lógico e às mesmas regras comerciais. O ganho está na repetibilidade: dois projetos na mesma versão do contrato têm tabelas, status e invariantes iguais, e toda diferença fica registrada em um mapeamento revisável.

Instalar esta skill não instala o módulo. Migrations, models, jobs, APIs e testes só existem no projeto consumidor depois de decisões e aprovação de escopo.

## Fluxo

1. **Identifique o modo:** `diagnosticar` (nenhuma alteração), `projeto_novo` ou `adequar_legado`. Revisão não vira implementação.
2. **Leia o projeto:** governança, ADRs, decisões, esquema atual, migrations e modelo de tenants. Não acesse `.env`, certificados ou segredos sem autorização. Identifique trabalho reservado a outros agentes.
3. **Combine com as outras skills:** use a skill de backend para padrões Laravel, a de frontend só em telas comerciais e a de coordenação para `PENDENCIAS.md`. Elas prevalecem nos seus temas; esta skill prevalece no contrato comercial.
4. **Gere a matriz de aderência** das 24 tabelas com [o modelo](templates/matriz-aderencia.md): `ATENDE`, `PARCIAL`, `AUSENTE`, `CONFLITANTE` ou `NÃO APLICÁVEL`, sempre com evidência de arquivo e coluna.
5. **Leve as decisões ausentes uma por vez,** com 2 a 4 opções, recomendação e impacto, conforme o [fluxo consultivo](references/fluxo-consultivo.md). Reutilize o que já foi decidido. Silêncio não é aprovação.
6. **Planeje por fase** com a [trilha de módulos](references/trilha-modulos.md). Módulo não contratado fica adiado, mantendo a nomenclatura do manifesto para não bloquear a adoção posterior.
7. **Com aprovação, implemente só a fase aprovada,** seguindo o [ADR](templates/adr-modulo.md). Nunca sobrescreva migration já executada.
8. **Verifique** com os [critérios de aceitação](references/criterios-aceitacao.md) e rode testes proporcionais. Falha de tenant, índice, integridade, idempotência ou contrato bloqueia a conclusão.
9. **Registre** a versão e o checksum em [registro de aplicação](templates/registro-aplicacao.yaml) e entregue o relatório abaixo.

## Onde está cada coisa

| Precisa de | Leia |
|---|---|
| Colunas, tipos, índices e fases, como fonte canônica | [schema-manifest.yaml](contracts/schema-manifest.yaml) |
| O mesmo conteúdo para leitura | [catálogo](contracts/catalogo-tabelas.md), [dicionário](contracts/dicionario-dados.md), [relacionamentos](contracts/relacionamentos.md), [índices](contracts/indices-restricoes.md) |
| Status e transições | [estados da assinatura](contracts/estados-assinatura.md) |
| Dinheiro, faturas, cupons, prorrateamento | [regras financeiras](contracts/regras-financeiras.md) |
| Eventos internos | [eventos de domínio](contracts/eventos-dominio.md) |
| API pública de planos | [OpenAPI](contracts/api-publica-openapi.yaml) |
| Versões, deriva e exceções | [compatibilidade](contracts/contratos-compatibilidade.md) |
| Projeto novo ou legado | [instalação](references/instalacao-projeto-novo.md), [adequação](references/adequacao-projeto-existente.md) |
| Tenants, provedores, LGPD, arquitetura | [isolamento](references/isolamentos-tenants.md), [provedores](references/provedores-pagamento.md), [segurança](references/seguranca-lgpd.md), [arquitetura](references/arquitetura-modular.md) |

## Invariantes

- **Fonte única de direitos:** versão contratada, itens e benefícios válidos, resolvidos no backend. Nada de `if` espalhado, variável de ambiente ou configuração de frontend, porque isso quebra quando o preço muda.
- **Contrato preservado:** catálogo novo gera versão nova. Assinaturas e itens guardam o que foi acordado e nunca são recalculados automaticamente.
- **Tenant fail-closed:** sem contexto validado, negue. Toda linha referenciada pertence ao mesmo tenant, inclusive IDs vindos da API.
- **Direito comercial não é permissão:** o plano define o teto do tenant; RBAC/ABAC define o usuário.
- **Dinheiro exato:** decimal em banco, string na API, nunca float. Cobrança idempotente; estorno é lançamento novo, e evento histórico não é apagado.
- **Ativação só por evento verificado:** o retorno do navegador não ativa plano pago.
- **Sem segredo nem dado de cartão:** nunca PAN/CVV; credencial nunca em texto puro; sandbox e produção separados.
- **Nada real sem autorização específica:** cobrança, envio de mensagem, migration destrutiva, deploy e `git push`.
- **Nada interno inventado:** `CompatBanco`, `RespostaApi`, `Route::crud`, `make:crud` e `gerar:modulo` não existem por presunção. Procure o equivalente no projeto.
- **Preço é dado:** valores de exemplo não viram constante nem verdade comercial.

Nomes e tipos do manifesto não variam por preferência do agente. Em legado, preserve contratos existentes e registre a adaptação no [mapeamento](templates/mapeamento-compatibilidade.yaml), com justificativa e teste, em vez de renomear de forma destrutiva.

## Relatório final

Sempre entregue: modo, versão da skill e checksum do manifesto (`python scripts/validar_skill.py --checksum`), matriz de aderência, decisões e ADRs, desvios aprovados, fases feitas e adiadas, arquivos alterados, comandos e resultados reais, riscos e pendências. Separe defeito comprovado de hipótese e declare o que não foi testado.

## Exemplo de invocação

> Use `$skill-saas-billing-mf` no modo diagnóstico para verificar o módulo comercial deste projeto contra o contrato v1.0.0. Não modifique arquivos nem execute migrations. Mostre a matriz das 24 tabelas, as decisões pendentes e o plano de ADRs.
