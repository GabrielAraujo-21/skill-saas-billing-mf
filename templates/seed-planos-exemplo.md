# Seed de planos — EXEMPLO COMERCIAL

**Estes valores são hipóteses de lançamento, não preços de mercado comprovados.** O projeto consumidor os substitui por decisão comercial própria. Nenhuma cobrança real parte deste seed.

| Plano | Slug | Modalidade | Mensal | Anual |
|---|---|---|---|---|
| Free | `free` | fixo | R$ 0,00 | R$ 0,00 |
| Starter | `starter` | fixo | R$ 59,90 | R$ 599,00 |
| Business | `business` | fixo | R$ 149,90 | R$ 1.499,00 |
| Enterprise | `enterprise` | a_partir_de | R$ 399,90 | R$ 3.999,00 |

## Regras do seed

- Opcional e idempotente: localiza por `slug` e `numero_versao`, sem duplicar nem alterar versão publicada.
- Cria a versão como `rascunho`; publicar é ação administrativa separada.
- Valores vêm de arquivo de dados ou configuração do seed, nunca de constante usada em regra de negócio.
- Trial de 14 dias é opção a ativar (`trial_dias = 14`); o padrão é 0.
- Funcionalidades e limites são definidos pelo projeto.
- Se o projeto usar orçamento em Enterprise, troque para `sob_consulta`, com `valor` nulo.
