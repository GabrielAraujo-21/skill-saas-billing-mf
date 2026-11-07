# Fluxo consultivo

## Como decidir

Primeiro procure a resposta nos ADRs, no `PENDENCIAS.md` e nas instruções do projeto. Pergunte só o que falta e afeta a etapa atual.

Apresente uma decisão por vez, em linguagem simples: o que é, por que decidir agora, 2 a 4 opções com ganhos e perdas, sua recomendação e o impacto no contrato. Registre a escolha antes da próxima. Silêncio não é aprovação.

## Decisões típicas

| Decisão | Afeta | Padrão sugerido |
|---|---|---|
| SGBD | Índice parcial, JSON, CHECK | O já usado pelo projeto |
| Nome e chave de tenants | Todas as FKs de tenant | Reutilizar a identidade existente; nunca criar uma segunda tabela |
| Padrão de IDs | Manifesto e mapeamento | `bigint`; outro tipo por ADR |
| Soft delete | `planos` e outras | Só `planos`; nunca em registro financeiro |
| PSP inicial | Fase 05 | Um provedor, escolhido após comparar a documentação oficial |
| Armazenamento de credenciais | `configuracao_referencia` | Cofre ou segredo do ambiente |
| Acesso ao faturamento | Policies | Papel específico, com negação por padrão |
| Retenção | Eventos, faturas, exportação | Definida com apoio jurídico |
| Tolerância e suspensão | Estados e acesso | Sem padrão universal |
| Prorrateamento, upgrade e downgrade | `assinaturas_alteracoes` | Sem padrão universal |
| Fases contratadas | Plano de execução | Só o necessário para vender agora |

## Reutilizável e específico

| Reutilizável (contrato) | Específico (ADR ou adaptador) |
|---|---|
| Tabelas, colunas, status, invariantes | SGBD, IDs, provedor, fases contratadas |
| Máquina de estados | Prazos de tolerância e retenção |
| Regras de dinheiro e idempotência | Preços, trial, cupons, política de excedente |
| Formato de eventos e API pública | Mecanismo de fila e layout de telas |
