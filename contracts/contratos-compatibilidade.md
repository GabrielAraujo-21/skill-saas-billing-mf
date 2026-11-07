# Compatibilidade do contrato

## Versões

`schema_version` segue versionamento semântico:

| Mudança | Exemplos | Versão |
|---|---|---|
| Correção sem efeito no esquema | Texto, exemplo | Patch |
| Expansão compatível | Coluna anulável, tabela, índice, novo valor de enumeração | Minor |
| Quebra | Remover ou renomear tabela, coluna ou status; mudar tipo ou unicidade | Major |

Quebra exige entrada no changelog e guia de migração expansiva e contrativa: adicionar, preencher, trocar a leitura e só depois remover.

## Registro no projeto consumidor

Cada projeto guarda o [registro de aplicação](../templates/registro-aplicacao.yaml), com a versão, o checksum do manifesto e as fases aplicadas. O checksum vem de `python scripts/validar_skill.py --checksum`, com finais de linha normalizados.

## Deriva de esquema

Deriva é qualquer diferença entre o banco e o manifesto que não esteja no mapeamento. Para detectá-la sem comparação visual, um teste do projeto consumidor lê o catálogo do banco e o compara ao manifesto mais o mapeamento, nas fases aplicadas. Tabela de fase adiada não é deriva.

## Mapeamento de exceções

Nomes e tipos do contrato não variam por preferência. Toda adaptação fica no [mapeamento versionado](../templates/mapeamento-compatibilidade.yaml), com motivo, aprovador e teste. São casos típicos:

- Legado com nomes consolidados, sem renomeação destrutiva.
- `tenants` e usuários com outro nome ou tipo de chave.
- ID não `bigint`, por ADR de chaves.
- Índice parcial substituído por técnica do SGBD.
- Isolamento em que `tenant_id` não se aplica, como instalação dedicada.

## Relação com as outras skills

O contrato segue as convenções de `skill-backend-mf`: identificadores em pt-BR sem acentos, dinheiro exato, instantes em UTC e isolamento fail-closed. Decisão registrada no projeto prevalece sobre um padrão, mas gera entrada no mapeamento quando altera o contrato.
