# Adequação de projeto existente

Modo `adequar_legado`: entender antes de mudar. Contratos em uso são preservados, e o caminho é sempre incremental e compatível.

## Inventário

Leia, sem alterar: migrations, models, rotas de cobrança, webhooks, jobs, integrações com provedores, modelo de tenants, ADRs e pendências. Identifique onde os direitos são decididos hoje, como `if`, configuração ou variáveis de ambiente. Dados reais só com autorização; prefira a estrutura ao conteúdo.

## Matriz

Preencha a [matriz de aderência](../templates/matriz-aderencia.md):

| Situação | Quando | Ação típica |
|---|---|---|
| `ATENDE` | Mesma semântica, estrutura e restrições | Nenhuma |
| `PARCIAL` | Falta coluna, índice ou regra | Migração expansiva |
| `AUSENTE` | Não existe | Criar na fase certa |
| `CONFLITANTE` | Semântica incompatível ou risco, como dinheiro em float | Decisão e plano próprio |
| `NÃO APLICÁVEL` | Módulo fora do negócio | Justificar e adiar |

Nome diferente com a mesma semântica é `ATENDE` com entrada no mapeamento, não motivo para renomear.

## Migração

Use o [plano de migração](../templates/plano-migracao.md), sempre em etapas expansivas e contrativas: adicionar, preencher em lotes, gravar nos dois lados se preciso, trocar a leitura e, em etapa aprovada à parte, remover. Nunca sobrescreva migration executada. Conversão de float em decimal exige conferência dos totais, antes e depois.

## Prioridade

Corrija antes: vazamento entre tenants, cobrança duplicada, ativação por retorno do navegador, webhook sem autenticação e segredo exposto. Não copie o padrão antigo para código novo, e não corrija fora do escopo sem pedido. Registre o que encontrar em `PENDENCIAS.md`.
