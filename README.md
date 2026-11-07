# skill-saas-billing-mf

Skill reutilizável que padroniza o módulo comercial de aplicações SaaS em Laravel: catálogo de planos, direitos de uso, assinaturas, faturas, pagamentos, consumo, adicionais e cupons, em um contrato canônico de 24 tabelas.

Ela é um conjunto de instruções e contratos. Não contém migrations executáveis, SDKs nem credenciais, e instalá-la não instala o módulo.

## Requisitos

- Nenhum para usar a skill.
- Python 3.9 ou superior apenas para o validador e os testes, que usam só a biblioteca padrão e não acessam a rede.
- No projeto consumidor, a stack de referência é a de `skill-backend-mf` 2.0.0: Laravel 13 com PHP 8.5 (8.4 quando a hospedagem exigir). Interfaces seguem `skill-frontend-mf` 2.0.0.

## Instalação em um projeto

Copie o conteúdo deste repositório, sem a pasta `.git`, para a pasta que o seu agente reconhece:

| Agente | Pasta no projeto |
|---|---|
| Claude Code | `.claude/skills/skill-saas-billing-mf/` |
| Codex | `.agents/skills/skill-saas-billing-mf/` |

```powershell
$origem = 'C:\caminho\skill-saas-billing-mf'
$destino = '.claude\skills\skill-saas-billing-mf'
New-Item -ItemType Directory -Force $destino | Out-Null
Get-ChildItem $origem -Force | Where-Object Name -ne '.git' | Copy-Item -Destination $destino -Recurse
```

Confirme com `python .claude/skills/skill-saas-billing-mf/scripts/validar_skill.py`. A cópia por projeto não acompanha atualizações: ao atualizar, substitua a pasta inteira e confira o checksum.

## Atualização de versão

1. Leia o [CHANGELOG](CHANGELOG.md) e a [política de compatibilidade](contracts/contratos-compatibilidade.md).
2. Substitua a cópia instalada.
3. Em cada projeto, compare o checksum com o [registro de aplicação](templates/registro-aplicacao.yaml). Mudança de contrato vira plano de migração próprio, nunca atualização automática.

## Exemplos de uso

**Projeto novo:**

> Use `$skill-saas-billing-mf` no modo `projeto_novo`. Leia as decisões registradas, leve as que faltam uma por vez e proponha o ADR da fase 01. Não crie migrations antes da aprovação.

**Legado:**

> Use `$skill-saas-billing-mf` no modo diagnóstico para verificar o módulo comercial deste projeto contra o contrato canônico v1.0.0. Não modifique arquivos nem execute migrations. Mostre a matriz de aderência das 24 tabelas, as decisões pendentes e o plano de ADRs. Utilize `$skill-backend-mf` para padrões Laravel e a skill de coordenação para controle de pendências. Após aprovação do escopo, implemente somente a primeira fase, com revisão e testes.

## Validação da skill

```bash
python scripts/validar_skill.py
```

```bash
python -m unittest discover -s tests
```

Depois de alterar `contracts/schema-manifest.yaml`, regenere os documentos com `python scripts/gerar_documentos.py`. O manifesto é a fonte; o validador reprova documentos gerados que tenham ficado para trás.

O manifesto é JSON, que também é YAML válido. Essa escolha permite ler o contrato sem instalar nada.

Estes testes validam a estrutura do contrato, inclusive em SQLite. Eles não comprovam o funcionamento do módulo em Laravel, que é testado no projeto consumidor. Os limites estão no [relatório de entrega](docs/relatorio-entrega-1.0.0.md).

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `contracts/` | Manifesto e contratos normativos |
| `references/` | Como aplicar o contrato |
| `templates/` | ADR, matriz, plano de migração, seed e registros |
| `tests/`, `scripts/` | Validação da própria skill |
| `docs/` | Revisão do prompt e relatório de entrega |

## Licença

[MIT](LICENSE).
