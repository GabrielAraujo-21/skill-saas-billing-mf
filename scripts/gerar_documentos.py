#!/usr/bin/env python3
"""Gera os contratos em Markdown a partir de contracts/schema-manifest.yaml, sem rede."""

import json
import sys
from pathlib import Path

AVISO = "> Arquivo gerado por `scripts/gerar_documentos.py` a partir de `schema-manifest.yaml`. Não editar à mão.\n"
GRUPOS = {
    "A": "Catálogo comercial",
    "B": "Contratação e utilização",
    "C": "Cobrança e pagamentos",
    "D": "Monetização complementar",
    "E": "Complementares padronizadas",
}


def carregar_manifesto(raiz):
    return json.loads((Path(raiz) / "contracts/schema-manifest.yaml").read_text(encoding="utf-8"))


def _celula(valor):
    return str(valor).replace("|", "\\|")


def _padrao(coluna):
    if "padrao" not in coluna:
        return "—"
    valor = coluna["padrao"]
    return str(valor).lower() if isinstance(valor, bool) else str(valor)


def catalogo(m):
    linhas = ["# Catálogo de tabelas", "", AVISO, f"Contrato `{m['schema_version']}`: 15 tabelas nucleares e 9 complementares.", ""]
    linhas += ["| # | Tabela | Grupo | Natureza | Fase | Escopo | Timestamps | Exclusão |", "|---|---|---|---|---|---|---|---|"]
    for t in m["tabelas"]:
        linhas.append(
            f"| {t['ordem']} | `{t['nome']}` | {GRUPOS[t['grupo']]} | {t['natureza']} | {t['fase']} | {t['escopo']} | {t['timestamps']} | {_celula(t['politica_exclusao'])} |"
        )
    linhas += ["", "## Fases", "", "| Fase | Módulo | Tabelas | Pré-condições | Gate |", "|---|---|---|---|---|"]
    for f in m["fases"]:
        tabelas = ", ".join(f"`{n}`" for n in f["tabelas"]) or "nenhuma"
        linhas.append(f"| {f['codigo']} | {f['modulo']} | {tabelas} | {f['pre_condicoes']} | {f['gate']} |")
    return "\n".join(linhas) + "\n"


def dicionario(m):
    linhas = ["# Dicionário de dados", "", AVISO, "## Convenções", ""]
    linhas += [f"- **{chave}:** {valor}" for chave, valor in m["convencoes"].items()]
    linhas += ["", "## Enumerações", "", "| Enumeração | Valores |", "|---|---|"]
    linhas += [f"| `{n}` | {', '.join(f'`{v}`' for v in vs)} |" for n, vs in m["enumeracoes"].items()]
    for t in m["tabelas"]:
        linhas += ["", f"## {t['ordem']}. `{t['nome']}`", ""]
        if "excecao_timestamps" in t:
            linhas += [f"Exceção de timestamps: {t['excecao_timestamps']}", ""]
        linhas += ["| Coluna | Tipo | Nulo | Padrão | Enum | Nota |", "|---|---|---|---|---|---|"]
        for c in t["colunas"]:
            linhas.append(
                f"| `{c['nome']}` | {c['tipo']} | {'sim' if c['nulo'] else 'não'} | {_padrao(c)} | {c.get('enum', '—')} | {_celula(c.get('nota', '—'))} |"
            )
    return "\n".join(linhas) + "\n"


def relacionamentos(m):
    linhas = ["# Relacionamentos", "", AVISO, "| Tabela | Coluna | Referencia | Nulo | ON DELETE | ON UPDATE |", "|---|---|---|---|---|---|"]
    for t in m["tabelas"]:
        for c in t["colunas"]:
            if "fk" in c:
                fk = c["fk"]
                linhas.append(
                    f"| `{t['nome']}` | `{c['nome']}` | `{fk['tabela']}.{fk['coluna']}` | {'sim' if c['nulo'] else 'não'} | {fk['on_delete']} | {fk['on_update']} |"
                )
    linhas += ["", "## Referências sem FK no contrato", "", "| Tabela | Coluna | Destino |", "|---|---|---|"]
    for t in m["tabelas"]:
        for c in t["colunas"]:
            if "referencia_externa" in c:
                linhas.append(f"| `{t['nome']}` | `{c['nome']}` | {c['referencia_externa']}, definido no mapeamento |")
    return "\n".join(linhas) + "\n"


def indices(m):
    linhas = ["# Índices e restrições", "", AVISO]
    for t in m["tabelas"]:
        linhas += [f"## `{t['nome']}`", ""]
        for u in t["unicos"]:
            condicao = f" onde `{u['condicao']}`" if "condicao" in u else ""
            linhas.append(f"- UNIQUE `{u['nome']}` ({', '.join(u['colunas'])}){condicao}")
        for i in t["indices"]:
            linhas.append(f"- INDEX `{i['nome']}` ({', '.join(i['colunas'])})")
        for c in t["checks"]:
            linhas.append(f"- CHECK `{c}`")
        linhas.append("")
    linhas += [
        "## Unicidade condicional e valores nulos",
        "",
        "PostgreSQL e SQLite aceitam `uq_assinaturas_tenant_efetiva` como índice parcial. No SQL Server, usar índice filtrado. No MySQL, usar coluna gerada que seja `tenant_id` nos status efetivos e NULL nos demais, com índice único nela, sem alterar o nome lógico da regra. Registrar a escolha no mapeamento e testá-la sob concorrência.",
        "",
        "Unicidades com coluna anulável permitem várias linhas com NULL. Isso é intencional em `transacao_externa_id`, `assinatura_externa_id`, `reembolso_externo_id` e `fatura_id`. O controle de cupom sem fatura é transacional, conforme `regras-financeiras.md`.",
    ]
    return "\n".join(linhas) + "\n"


def estados(m):
    q = m["maquina_estados_assinatura"]
    linhas = ["# Estados da assinatura", "", AVISO]
    linhas += [f"- **Iniciais:** {', '.join(q['iniciais'])}.", f"- **Efetivos (no máximo um por tenant):** {', '.join(q['efetivos'])}.", f"- **Terminais:** {', '.join(q['terminais'])}. Reativar depois deles cria nova assinatura.", ""]
    linhas += ["## Transições permitidas", "", "| De | Para | Gatilho |", "|---|---|---|"]
    linhas += [f"| `{t['de']}` | `{t['para']}` | {t['gatilho']} |" for t in q["transicoes"]]
    linhas += ["", "Qualquer outra transição é recusada e registrada. Evento fora de ordem não regride um estado confirmado.", ""]
    linhas += ["## Efeitos de acesso", "", "| Estado | Efeito |", "|---|---|"]
    linhas += [f"| `{e}` | {x} |" for e, x in q["efeitos_acesso"].items()]
    linhas += ["", "O efeito define o teto comercial; a permissão do usuário continua vindo de RBAC/ABAC."]
    return "\n".join(linhas) + "\n"


GERADOS = {
    "contracts/catalogo-tabelas.md": catalogo,
    "contracts/dicionario-dados.md": dicionario,
    "contracts/relacionamentos.md": relacionamentos,
    "contracts/indices-restricoes.md": indices,
    "contracts/estados-assinatura.md": estados,
}


def divergencias(raiz, manifesto=None):
    raiz = Path(raiz)
    m = manifesto or carregar_manifesto(raiz)
    saida = []
    for caminho, gerador in GERADOS.items():
        alvo = raiz / caminho
        if not alvo.is_file() or alvo.read_text(encoding="utf-8") != gerador(m):
            saida.append(caminho)
    return saida


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parents[1]
    if "--verificar" in sys.argv:
        problemas = divergencias(raiz)
        for caminho in problemas:
            print(f"DIVERGENTE: {caminho}")
        sys.exit(1 if problemas else 0)
    manifesto = carregar_manifesto(raiz)
    for caminho, gerador in GERADOS.items():
        (raiz / caminho).write_text(gerador(manifesto), encoding="utf-8", newline="\n")
        print(f"Gerado: {caminho}")
