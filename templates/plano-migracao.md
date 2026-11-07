# Plano de migração

**Fase:** NN | **ADR:** link | **Contrato:** versão de origem e de destino

## Situação atual

Estruturas, volume aproximado e dependências, sem dados pessoais.

## Etapas

| # | Tipo | Ação | Reversível? | Como verificar |
|---|---|---|---|---|
| 1 | Expansão | Adicionar sem remover nada | | |
| 2 | Dados | Preencher em lotes, de forma idempotente | | |
| 3 | Troca | Mudar a leitura, com flag se preciso | | |
| 4 | Contração | Remover o antigo, em aprovação separada | | |

## Conferência de dados

Totais e contagens antes e depois, por tenant e moeda. Divergência interrompe o plano.

## Rollback

Ponto de não retorno, restauração e responsáveis. Backup testado antes de etapa destrutiva.

## Autorizações

Migration destrutiva, ambiente real e janela exigem aprovação específica.
