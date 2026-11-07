# Relatório de entrega — 1.0.0

Data: 2026-11-03.

## Resultado do validador e dos testes

Executados em contêiner `python:3.13-slim`, sem rede (`--network none`).

| Verificação | Resultado |
|---|---|
| `python scripts/validar_skill.py` | Aprovado, com manifesto sha256 `7dc187f5f5d15d6e52e93ab401c962d31d1c58572455e981d2db99f0485099a8` |
| `python -m unittest discover -s tests` | 42 testes aprovados |

## O que foi comprovado

- O manifesto tem 24 tabelas consistentes, e as FKs respeitam a ordem das fases.
- O esquema é criado em SQLite, fase a fase, com as FKs ativas.
- As restrições recusam: segunda assinatura efetiva, status inválido, tenant inexistente, webhook duplicado, baixa duplicada, consumo repetido, cupom repetido na fatura e exclusão de dado financeiro.
- O validador reprova a remoção de tabela, FK, status ou nome obrigatório, além de documentos fora de sincronia.

## O que não foi comprovado

| Item | Situação |
|---|---|
| Migrations Laravel, API, policies e jobs | Não existem nesta skill; são gerados e testados no projeto consumidor |
| PostgreSQL, MySQL e SQL Server | Não executado; só SQLite |
| Concorrência real | Não executado; SQLite em memória não a exercita |
| Provedores reais | Sem chamadas; a documentação oficial deve ser lida antes de implementar, e só a resposta dos links foi conferida |
| Validação formal do OpenAPI | Só verificação textual, sem ferramenta de validação |
| Comportamento de um agente com a skill | Cenários escritos em `tests/fixtures/projetos-exemplo.md`, sem execução comparativa |

## Matriz de conformidade com o prompt

| Exigência | Situação |
|---|---|
| Estrutura física da seção 2 | Atendida, com acréscimos justificados |
| 24 tabelas com colunas completas | Atendida, com as alterações de [revisao-prompt.md](revisao-prompt.md) |
| Invariantes da seção 4 | Atendidas nos contratos; as de execução dependem do projeto consumidor |
| Fases, ADRs e gates | Atendidos, com duas tabelas realocadas |
| Comportamento e relatório da seção 6 | Atendidos em `SKILL.md` |
| Seeds de exemplo | Atendidos como modelo, sem executável |
| Validador e fixtures negativas | Atendidos |
| Laboratório de migrations e API | **Parcial:** SQLite para migrations; API não testada |
| Exemplos de invocação | Atendidos |

## Riscos

- O contrato só será posto à prova de verdade na primeira aplicação em Laravel; espere ajustes em uma versão 1.0.x ou 1.1.
- Os testes em SQLite não garantem o mesmo comportamento em outro SGBD, especialmente no índice parcial em MySQL.
- As enumerações definidas na revisão não passaram por validação comercial.

## Decisões ainda necessárias

- Publicar ou não o repositório, e onde. Nenhum remoto foi configurado.
- Por projeto: as decisões de [fluxo consultivo](../references/fluxo-consultivo.md).
